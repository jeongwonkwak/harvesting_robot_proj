import base64                                    
                                                
input_path = "/home/user/사진/딸기.jpg"          
output_path = "/home/user/사진/딸기_base64.txt"
                                                
with open(input_path, "rb") as f:                
    encoded = base64.b64encode(f.read()).decode("utf-8")       
                                                
with open(output_path, "w") as f:                
    f.write(encoded)
                                                
print(f"저장 완료: {output_path}") 