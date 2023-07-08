from random import randint

def num_0_to_4():

    num0 = str(randint(10000000, 12000000))
    num1 = str(randint(2000, 2100))
    num2 = str(randint(1, 12))
    num3 = str(randint(1, 31))
    num4 = str(randint(1, 10000))

    return num0,num1,num2,num3,num4

print(num_0_to_4())

## 22번 : 면허종별 - "「의료법」에서는 처방전 발급 의무의 주체를 “의사 또는 치과의사”로 규정하고 해당 “의사 또는 치과의사”가 발급하는 처방전의 서식 등에 관해 규정"
## 한의사의 경우 처방전 발급 의무는 없으나 한약사에게 조제 요청을 위해 처방전을 발급하는 경우가 있음. (이 경우 약 이름은 한글이겠지요?) 
def num_22():
    license_list = ["의사", "치과의사", "한의사"]
    n = randint(0,2)
    return license_list[n]

print(num_22())


## 23번 면허 번호 : 6자리 숫자
def num_23():
    num23 = str(randint(100000,999999))

    return num23

print(num_23())




