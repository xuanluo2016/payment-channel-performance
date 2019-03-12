
from flask import Flask
from get_data import get_summary

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    get_summary()
    app.run(host='0.0.0.0')

    # mapper = Code("""
    #             function () {
    #                 emit(this.actual_cost, (this.waiting_time + this.waiting_mined_time)); 
    #                 });
    #             }
    #             """)

    # reducer = Code("""
    #                 function (key, values) {
    #                     return Array.avg(values) 
    #                 }
    #                 """)

    # result = db.things.map_reduce(mapper, reducer, "test_mapreduce")
    # for doc in result.find():
    #     pprint.pprint(doc)







