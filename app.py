#!/usr/bin/python


from flask import Flask, jsonify, abort, make_response, request
app = Flask(__name__)

icn_services = [ 
        {   
            'id': 0,
            'name': 'vfsr-conference-huawei',
            'virtual_machines': [
                    {'VM':
                                {   
                                    'vm_ip': '10.1.1.2',
                                    'vm_name': 'vfsr-conference-huawei-2',
                                    'vm_zone': 'zone-1'
                                }   
                    },  
                    {'VM':
                                {   
                                    'vm_ip': '10.1.1.2',
                                    'vm_name': 'vfsr-conference-huawei-2',
                                    'vm_zone': 'zone-1'
                                }   
                    }   
                ],  
            'prefix': 'ccnx:/cona/chat-room/huawei',
            'min_clients': 120,
            'max_clients': 200 
        },  
        {   
            'id': 1,
            'name': 'vfsr-conference-huawei',
            'virtual_machines': [
                    {'VM':
                                {   
                                    'vm_ip': '10.1.1.4',
                                    'vm_name': 'vfsr-conference-huawei-2',
                                    'vm_zone': 'zone-1'
                                }   
                    },  
                    {'VM':
                                {   
                                    'vm_ip': '10.1.1.5',
                                    'vm_name': 'vfsr-conference-huawei-2',
                                    'vm_zone': 'zone-1'
                                }   
                    }   
                ],  
            'prefix': 'ccnx:/cona/chat-room/huawei',
            'min_clients': 220,
            'max_clients': 200
        },
    ]

@app.route('/icn/apis/v1.0/services/<int:service_id>', methods = ['PUT'])
def update_service(service_id):
    icn_service = filter(lambda t: t['id'] == service_id, icn_services)
    if len(icn_service) == 0:
        abort(404)
    if not request.json:
        abort(400)
    #print icn_service //return a list of dict
    #print icn_service[0] //return a dict contating all the data
    icn_service[0]['name'] = request.json.get('name', icn_service[0]['name'])

    for key, value in icn_service[0].items():
        print "%s: %s" % (key, value)
    print "udpate service: %s" % icn_service[0]['id']
    return jsonify({'icn_service': icn_service[0]})

@app.route('/icn/apis/v1.0/services/<int:service_id>', methods = ['DELETE'])
def delete_service(service_id):
    icn_service = filter(lambda t: t['id'] == service_id, icn_services)
    if len(icn_service) == 0:
        abort(404)
    icn_services.remove(icn_service[0])
    print "delete service: %s" % icn_service[0]['id']
    return jsonify({ 'Result': True })
    
@app.route('/icn/apis/v1.0/services/<int:service_id>', methods = ['GET'])
def get_service(service_id):
    service = filter(lambda t: t['id'] == service_id, icn_services)
    if len(service) == 0:
        abort(404)
    return jsonify({'service': service } )

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( {'Error': 'Not Found'} ), 404)

@app.route('/icn/apis/v1.0/services', methods=['GET'])
def get_services():
    return jsonify( {'ICN_Services': icn_services} )

@app.route('/icn/apis/v1.0/services', methods=['POST'])
def create_service():
    if not request.json or not 'id' in request.json:
        abort(400)
    icn_service = {
                'id': request.json['id'],
                'name': request.json['name']
            }
    icn_services.append( icn_service )
    print "create service: %s" % icn_service['id']
    return jsonify( {'icn_service': icn_service} ), 201

if __name__ == '__main__':
    print '__name__ = ', __name__
    app.run('192.168.1.140', 5000, debug=True)
                                                
