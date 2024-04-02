from app.routes.student import student_api

#print(student_api.all_records().json)
#print(student_api.single_record(1).json)

postDict = {
"name":"Salvatore Amaddio",
"nationality": "Italian",
"city": "London",
"lat": "51.582964",
"long":"-0.086066",
"gender": "M",
"age": "30",
"english_grade": "9",
"math_grade": "6",
"sciences_grade": "8",
"languages_grade": "9"
}
#print(student_api.post_record(1,postDict).json)

putDict = {
"name":"Salvatore Amaddio Rivolta",
"nationality": "Italian",
"city": "London",
"lat": "51.582964",
"long":"-0.086066",
"gender": "M",
"age": "30",
"english_grade": "9",
"math_grade": "6",
"sciences_grade": "8",
"languages_grade": "9"
}
#print(student_api.put_record(1,putDict).json)

patchDict = {
"name":"Salvo",
}
#print(student_api.patc_record(1,patchDict).json)