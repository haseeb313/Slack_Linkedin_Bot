
import datetime
import json
from time import sleep
import demoji
import slack
from linkedin_slack_bot.linkedin import API_Linkedin



class Linkedin_Bot(API_Linkedin):
    def __init__(self, username, password, slack_token , channel_name , interval):
        self.api = API_Linkedin( username, password)
        self.client_slack = slack.WebClient(token = slack_token)
        self.interval = interval
        self.channel = channel_name



    def run(self):

        # SLACK_TOKEN="xoxb-5469333287683-5496943101283-FVMsWsFXNu3PEiISChzJXEt4"    

        # api = API_Linkedin('crackpots313@gmail.com', 'Warid@123')

        # client_slack = slack.WebClient(token = SLACK_TOKEN)

        processed_tracking_ids = list()

        max_elements = 25



        while True:
            search = self.api.get_conversations(0 , 25)

            encoded_str = json.dumps(search, ensure_ascii=False).encode('utf-8')
            decoded_str = encoded_str.decode('utf-8')
            no_emoji_str = demoji.replace(decoded_str, '')
            

            parsed_data = json.loads(no_emoji_str)



            if "elements" in search:        
                for m in parsed_data["elements"]:
                    current_time = datetime.datetime.now()
                    
                    created_t = m["events"][0]["createdAt"]
                    created_dt = datetime.datetime.fromtimestamp(created_t / 1000)            
                    time_difference = (current_time - created_dt).total_seconds()            
                    s = m["events"][0]
                    entity = s["entityUrn"].split(":")[3]


                    if ((m['unreadCount'] == 1) and (s['subtype'] == "MEMBER_TO_MEMBER" or s['subtype'] == "INMAIL") and time_difference <= (self.interval + 40) and entity not in processed_tracking_ids):
                                            
                        text = s["eventContent"]["com.linkedin.voyager.messaging.event.MessageEvent"]["attributedBody"]["text"]
                        sender = s['from']['com.linkedin.voyager.messaging.MessagingMember']['miniProfile']
                        se_f = sender['firstName']
                        se_l = sender['lastName']
                        formatted_datetime = created_dt.strftime("%d-%m-%Y %I:%M %p")
                        text_send = f"({formatted_datetime}) {se_f} {se_l} : '{text}'"
                        print(text_send)
                        self.client_slack.chat_postMessage(channel= self.channel , text = text_send)
                        processed_tracking_ids.append(entity)
                    
                    


                    if m['unreadCount'] > 1:
                        conver_urn = m['dashEntityUrn'].split(":")[3]                
                        search_con = self.api.get_conversation(conver_urn)
                        encoded_str_con = json.dumps(search_con, ensure_ascii=False).encode('utf-8')
                        decoded_str_con = encoded_str_con.decode('utf-8')
                        no_emoji_str_con = demoji.replace(decoded_str_con, '')
                        parsed_data_con = json.loads(no_emoji_str_con)

                        for n in parsed_data_con["elements"]:
                            current_time_con = datetime.datetime.now()
                            
                            created_t_con = n["createdAt"]
                            created_dt_con = datetime.datetime.fromtimestamp(created_t_con / 1000)                    
                            time_difference_con = (current_time_con - created_dt_con).total_seconds()                   
                            entity_con = n["entityUrn"].split(":")[3]

                            if time_difference_con <= (self.interval + 40) and entity_con not in processed_tracking_ids:
                                text = n["eventContent"]["com.linkedin.voyager.messaging.event.MessageEvent"]["attributedBody"]["text"]
                                sender = n['from']['com.linkedin.voyager.messaging.MessagingMember']['miniProfile']
                                se_f = sender['firstName']
                                se_l = sender['lastName']
                                formatted_datetime_con = created_dt_con.strftime("%d-%m-%Y %I:%M %p")
                                text_send_con = f"({formatted_datetime_con}) {se_f} {se_l} : '{text}'"
                                print(text_send_con)
                                self.client_slack.chat_postMessage(channel= self.channel ,text = text_send_con)
                                processed_tracking_ids.append(entity_con)

                
            else:
                print("No conversations found.")

            if len(processed_tracking_ids) > max_elements:
                excess_elements = len(processed_tracking_ids) - max_elements
                my_list = processed_tracking_ids[excess_elements:]
            

            sleep(self.interval)


