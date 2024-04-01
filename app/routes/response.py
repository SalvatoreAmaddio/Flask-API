from flask import jsonify

def response(*args): 
    if len(args) == 2:
        return jsonify(information=args[0], status_code=args[1]), args[1]
    elif len(args)==3:
        return jsonify(msg=args[0], data=args[1], status_code=args[2]), args[2]
