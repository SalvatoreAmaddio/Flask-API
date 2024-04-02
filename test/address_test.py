from app.routes.address import address_api

#print(address_api.all_records().json)
#print(address_api.single_record(1).json)

postDict = { 
"student_id": "1",
"number": "79",
"house_name": "The Grove",
"road": "North Grove",
"city": "London",
"state": "England",
"country": "United Kingdom",
"zipcode": "N15 5QS"
}

#print(address_api.post_record(1,postDict).json)

putDict = {
"student_id": "1",
"number": "80",
"house_name": "The Grove",
"road": "North Grove",
"city": "London",
"state": "England",
"country": "United Kingdom",
"zipcode": "N15 5QS"
}

#print(address_api.put_record(1,putDict).json)

patchDict = {
"number":"90",
}
#print(address_api.patc_record(1,patchDict).json)