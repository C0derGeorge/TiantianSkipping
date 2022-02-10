import json
import random

import mitmproxy.http

event_example = {
    "action_name": "JumpRopeAction",
    "begin_time": 0,
    "end_time": 0,
    "score": 1.0,
    "succ_count": 0,
    "take_time": 300  # 每一次跳跃间隔时间，单位ms，过小会导致请求过长
}


class Main:
    def request(self, flow: mitmproxy.http.HTTPFlow):
        if "https://api.tiantiantiaosheng.com/api/user/drill_record_upload" == flow.request.url:
            content = json.loads(flow.request.text)
            count = 60000 // event_example["take_time"]  # 跳绳个数

            for _ in range(count):
                try:
                    new_event_time = content["interactions"][-1]["end_time"]
                except (KeyError, IndexError):
                    new_event_time = content["begin_time"]

                new_event = event_example
                new_event["begin_time"] = new_event_time
                new_event["end_time"] = new_event_time + new_event["take_time"]
                content["interactions"].append(new_event)
            content["max_combo_count"] = count
            content["interrupt_count"] = 0
            content["single_leg_count"] = 1  # 似乎是单腿跳
            content["succ_count"] = count
            content["take_time"] = new_event_time - content["begin_time"]
            content["body_detect_count"] = random.randint(300, 1200)
            content["end_time"] = new_event_time
            content["error_count"] = 0
            print(content)

            flow.request.set_text(json.dumps(content))


addons = [
    Main()
]
