from typing import Literal
from slack_app.utils import get_nocontext_response, get_feedback_repsponse, get_loading_text

def get_hello_block(fname: str):
    return [{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"Hi {fname}, Welcome to Ask Angela, your assistant for HR queries. Ask any question and get answers in seconds! Please note that Ask Angela is still in development. If you believe an answer may be incorrect, we recommend verifying it with your HRBP directly."
        }
    }]
    
def get_loading_block():
    loading_response = get_loading_text()
    return [{
        "type": "section",
        "text": {
            "type": "mrkdwn", 
            "text": f"> {loading_response}"
        }
    }]

def get_response_block(response: str):
    return [{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": response        
        }
    }]

def get_response_block_with_actions(response: str, type: Literal["no_context", None] = None):
    response_blocks = [{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": response        
        }
    }]

    if type == "no_context":
        nocontext_response = get_nocontext_response()
        response_blocks.extend([
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{nocontext_response}"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Raise Ticket",
                            "emoji": True
                        },
                        # "url": "https://hrsupport.angelone.in/hc/en-us/requests/new?ticket_form_id=5893162753309",
                        "action_id": "open_form_button"
                    }
                ]
            }
        ])
    else:
        default_response = get_feedback_repsponse()
        response_blocks.extend([
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{default_response}"
                }
            }, {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "👍"
                        },
                        "value": "thumbs_up",
                        "action_id": "feedback_thumbs_up"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "👎"
                        },
                        "value": "thumbs_down",
                        "action_id": "feedback_thumbs_down"
                    }
                ]
            }
        ])
    
    return response_blocks

def get_feedback_block(type: Literal["no_context", None] = None):
    if type == "no_context":
        nocontext_response = get_nocontext_response()
        return [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{nocontext_response}"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Raise Ticket",
                            "emoji": True
                        },
                        "url": "https://hrsupport.angelone.in/hc/en-us/requests/new?ticket_form_id=5893162753309",
                        "action_id": "raise_ticket_click"
                    }
                ]
            }
        ]
    else:
        default_response = get_feedback_repsponse()
        return [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{default_response}"
                }
            }, {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "👍"
                        },
                        "value": "thumbs_up",
                        "action_id": "feedback_thumbs_up"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "👎"
                        },
                        "value": "thumbs_down",
                        "action_id": "feedback_thumbs_down"
                    }
                ]
            }
        ]
        
def get_actions_block(type: Literal["thumbs_up", "thumbs_down"]):
    if type == "thumbs_down":
        nocontext_response = get_nocontext_response(type="actions")
        return [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{nocontext_response}"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Raise Ticket",
                            "emoji": True
                        },
                        # "url": "https://hrsupport.angelone.in/hc/en-us/requests/new?ticket_form_id=5893162753309",
                        "action_id": "open_form_button"
                    }
                ]
            }
        ]
    else:
        return [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Thank you so much for your positive feedback."
                }
            }
        ]
        
def get_form_blocks():
    return [
            {
                "type": "input",
                "block_id": "form_category",
                "label": {
                    "type": "plain_text",
                    "text": "Please choose your issue below"
                },
                "element": {
                    "type": "static_select",
                    "action_id": "dropdown_action",
                    "placeholder": {
                    "type": "plain_text",
                    "text": "Select an option"
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Employee Greviences"
                            },
                            "value": "employee_greviences"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "HR Assist"
                            },
                            "value": "hr_assist"
                        }
                    ],
                    "initial_option": {
                        "text": {
                            "type": "plain_text",
                            "text": "HR Assist"
                        },
                        "value": "hr_assist"
                    }
                }
            },
            {
                "type": "input",
                "block_id": "request_category",
                "label": {
                    "type": "plain_text",
                    "text": "HR Service Category"
                },
                "element": {
                    "type": "static_select",
                    "action_id": "dropdown_action",
                    "placeholder": {
                    "type": "plain_text",
                    "text": "Select an option"
                    },
                    "options": [
                        {
                            "text": {
                            "type": "plain_text",
                            "text": "Attendence and Leave"
                            },
                            "value": "attendence_and_leave"
                        },
                    ],
                    "initial_option": {
                        "text": {
                            "type": "plain_text",
                            "text": "Attendence and Leave"
                        },
                        "value": "attendence_and_leave"
                    }
                }
            },
            {
                "type": "input",
                "block_id": "request_sub_category",
                "label": {
                    "type": "plain_text",
                    "text": "Service Sub Category"
                },
                "element": {
                    "type": "static_select",
                    "action_id": "dropdown_action",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an option"
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Clock-In/Clock-Out Issue"
                            },
                            "value": "clock_in_and_out_issue"
                        },
                    ],
                    "initial_option": {
                        "text": {
                            "type": "plain_text",
                            "text": "Clock-In/Clock-Out Issue"
                        },
                        "value": "clock_in_and_out_issue"
                    }
                }
            }, 
            {
                "type": "input",
                "block_id": "subject",
                "label": {
                    "type": "plain_text",
                    "text": "Subject"
                },
                "element": {
                    "type": "plain_text_input",
                    "action_id": "feedback_input",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Write your feedback here..."
                    }
                }
            },
            {
                "type": "input",
                "block_id": "discription",
                "label": {
                    "type": "plain_text",
                    "text": "Discription"
                },
                "element": {
                    "type": "plain_text_input",
                    "action_id": "feedback_input",
                    "multiline": True,
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Write your feedback here..."
                    }
                }
            }
        ]