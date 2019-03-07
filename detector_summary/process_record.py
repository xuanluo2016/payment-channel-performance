def process_record(col_start_time,col_end_time,col_summary,record):
    if('starttime' in record):
        return process_record_assistant1(col_start_time,col_end_time,col_summary,record)
        
    if('blocktime' in record):
        return process_record_assistant2(col_start_time,col_end_time,col_summary,record)

def process_record_assistant1(col_start_time,col_end_time,col_summary,record):
    """
    Check if the txhash exists or not in the end_time table
    if yes, send streaming data to query tx details and remove related record in the end_time db
    else, save data in the start_time db
    """
    if('txhash' in record): 
        doc = col_end_time.find_one({"txhash": record['txhash']} )
        try: 
            if(doc != None):
                end_time = doc['blocktime']

                start_time = record['seconds']
                end_time =  int(end_time, 16)
                waiting_mined_time = end_time - start_time
                row = {"txhash": record['txhash'], "blocknumber": doc['blocknumber'], "blocktime": end_time,"waiting_time": 0.0,"actual_cost": 0.0, "gas_price":0.0, "waiting_mined_time": waiting_mined_time}        
                result = col_summary.insert_one(row)
                print('inserted')
                return 0
            else:
                print("insert into start_time")
                # Insert the item to start_time db, ignore the item if duplicate
                col_start_time.insert(record)
                return 1
        except:
            pass

        finally:
            return -1
            
    return -1

def process_record_assistant2(col_start_time,col_end_time,col_summary,record):
    """
    Check if the txhash exists or not in the end_time table
    if yes, send streaming data to query tx details and remove related record in the end_time db
    else, save data in the start_time db
    """
    if('txhash' in record): 
        doc = col_start_time.find_one({"txhash": record['txhash']} )
        try: 
            if(doc != None):
                # Send tx, start_time, end_time for further processing
                start_time = doc['seconds']

                end_time = record['blocktime']
                end_time = int(end_time,16)
                waiting_mined_time = end_time - start_time
                row = {"txhash": record['txhash'], "blocknumber": record['blocknumber'], "blocktime": end_time,"waiting_time": 0.0,"actual_cost": 0.0, "gas_price":0.0, "waiting_mined_time": waiting_mined_time}        
                result = col_summary.insert_one(row)
                print('inserted')
                return 0
            else:
                print("insert into end_time")
                # Insert the item to start_time db, ignore the item if duplicate
                col_end_time.insert(record)
                return 1
        except Exception as e:
            print(e)

        finally:
            return -1
            
    return -1