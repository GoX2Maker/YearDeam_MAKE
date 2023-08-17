 # -*- coding: utf-8 -*-
import random
import cv2
import pandas as pd
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import json
from tqdm.auto import tqdm
import time
import os
import shutil
import re
import glob
from natsort import natsorted

class DataSet():
    def __init__(self, saveIMGPath, saveJsonPath,savepathConvertIMG_Resnet, savepathConvertLBL_Resnet,dbPath, medicinePath, labelingPath, imgPath):
        self.saveIMGPath = saveIMGPath
        self.saveJsonPath = saveJsonPath
        self.savepathConvertIMG_Resnet = savepathConvertIMG_Resnet
        self.savepathConvertLBL_Resnet = savepathConvertLBL_Resnet
        self.medicine_df = pd.read_csv(medicinePath)
        self.position_df = pd.read_csv(dbPath)
        self.labeling_df = pd.read_json(labelingPath)
        self.prescription_img = cv2.imread(imgPath)
        self.kor = set("가각간갇갈갉갊감갑값갓갔강갖갗같갚갛개객갠갤갬갭갯갰갱갸갹갼걀걋걍걔걘걜거걱건걷걸걺검겁것겄겅겆겉겊겋게겐겔겜겝겟겠겡겨격겪견겯결겸겹겻겼경곁계곈곌곕곗고곡곤곧골곪곬곯곰곱곳공곶과곽관괄괆괌괍괏광괘괜괠괩괬괭괴괵괸괼굄굅굇굉교굔굘굡굣구국군굳굴굵굶굻굼굽굿궁궂궈궉권궐궜궝궤궷귀귁귄귈귐귑귓규균귤그극근귿글긁금급긋긍긔기긱긴긷길긺김깁깃깅깆깊까깍깎깐깔깖깜깝깟깠깡깥깨깩깬깰깸깹깻깼깽꺄꺅꺌꺼꺽꺾껀껄껌껍껏껐껑께껙껜껨껫껭껴껸껼꼇꼈꼍꼐꼬꼭꼰꼲꼴꼼꼽꼿꽁꽂꽃꽈꽉꽐꽜꽝꽤꽥꽹꾀꾄꾈꾐꾑꾕꾜꾸꾹꾼꿀꿇꿈꿉꿋꿍꿎꿔꿜꿨꿩꿰꿱꿴꿸뀀뀁뀄뀌뀐뀔뀜뀝뀨끄끅끈끊끌끎끓끔끕끗끙끝끼끽낀낄낌낍낏낑나낙낚난낟날낡낢남납낫났낭낮낯낱낳내낵낸낼냄냅냇냈냉냐냑냔냘냠냥너넉넋넌널넒넓넘넙넛넜넝넣네넥넨넬넴넵넷넸넹녀녁년녈념녑녔녕녘녜녠노녹논놀놂놈놉놋농높놓놔놘놜놨뇌뇐뇔뇜뇝뇟뇨뇩뇬뇰뇹뇻뇽누눅눈눋눌눔눕눗눙눠눴눼뉘뉜뉠뉨뉩뉴뉵뉼늄늅늉느늑는늘늙늚늠늡늣능늦늪늬늰늴니닉닌닐닒님닙닛닝닢다닥닦단닫달닭닮닯닳담답닷닸당닺닻닿대댁댄댈댐댑댓댔댕댜더덕덖던덛덜덞덟덤덥덧덩덫덮데덱덴델뎀뎁뎃뎄뎅뎌뎐뎔뎠뎡뎨뎬도독돈돋돌돎돐돔돕돗동돛돝돠돤돨돼됐되된될됨됩됫됴두둑둔둘둠둡둣둥둬뒀뒈뒝뒤뒨뒬뒵뒷뒹듀듄듈듐듕드득든듣들듦듬듭듯등듸디딕딘딛딜딤딥딧딨딩딪따딱딴딸땀땁땃땄땅땋때땍땐땔땜땝땟땠땡떠떡떤떨떪떫떰떱떳떴떵떻떼떽뗀뗄뗌뗍뗏뗐뗑뗘뗬또똑똔똘똥똬똴뙈뙤뙨뚜뚝뚠뚤뚫뚬뚱뛔뛰뛴뛸뜀뜁뜅뜨뜩뜬뜯뜰뜸뜹뜻띄띈띌띔띕띠띤띨띰띱띳띵라락란랄람랍랏랐랑랒랖랗래랙랜랠램랩랫랬랭랴략랸럇량러럭런럴럼럽럿렀렁렇레렉렌렐렘렙렛렝려력련렬렴렵렷렸령례롄롑롓로록론롤롬롭롯롱롸롼뢍뢨뢰뢴뢸룀룁룃룅료룐룔룝룟룡루룩룬룰룸룹룻룽뤄뤘뤠뤼뤽륀륄륌륏륑류륙륜률륨륩륫륭르륵른를름릅릇릉릊릍릎리릭린릴림립릿링마막만많맏말맑맒맘맙맛망맞맡맣매맥맨맬맴맵맷맸맹맺먀먁먈먕머먹먼멀멂멈멉멋멍멎멓메멕멘멜멤멥멧멨멩며멱면멸몃몄명몇몌모목몫몬몰몲몸몹못몽뫄뫈뫘뫙뫼묀묄묍묏묑묘묜묠묩묫무묵묶문묻물묽묾뭄뭅뭇뭉뭍뭏뭐뭔뭘뭡뭣뭬뮈뮌뮐뮤뮨뮬뮴뮷므믄믈믐믓미믹민믿밀밂밈밉밋밌밍및밑바박밖밗반받발밝밞밟밤밥밧방밭배백밴밸뱀뱁뱃뱄뱅뱉뱌뱍뱐뱝버벅번벋벌벎범법벗벙벚베벡벤벧벨벰벱벳벴벵벼벽변별볍볏볐병볕볘볜보복볶본볼봄봅봇봉봐봔봤봬뵀뵈뵉뵌뵐뵘뵙뵤뵨부북분붇불붉붊붐붑붓붕붙붚붜붤붰붸뷔뷕뷘뷜뷩뷰뷴뷸븀븃븅브븍븐블븜븝븟비빅빈빌빎빔빕빗빙빚빛빠빡빤빨빪빰빱빳빴빵빻빼빽뺀뺄뺌뺍뺏뺐뺑뺘뺙뺨뻐뻑뻔뻗뻘뻠뻣뻤뻥뻬뼁뼈뼉뼘뼙뼛뼜뼝뽀뽁뽄뽈뽐뽑뽕뾔뾰뿅뿌뿍뿐뿔뿜뿟뿡쀼쁑쁘쁜쁠쁨쁩삐삑삔삘삠삡삣삥사삭삯산삳살삵삶삼삽삿샀상샅새색샌샐샘샙샛샜생샤샥샨샬샴샵샷샹섀섄섈섐섕서석섞섟선섣설섦섧섬섭섯섰성섶세섹센셀셈셉셋셌셍셔셕션셜셤셥셧셨셩셰셴셸솅소속솎손솔솖솜솝솟송솥솨솩솬솰솽쇄쇈쇌쇔쇗쇘쇠쇤쇨쇰쇱쇳쇼쇽숀숄숌숍숏숑수숙순숟술숨숩숫숭숯숱숲숴쉈쉐쉑쉔쉘쉠쉥쉬쉭쉰쉴쉼쉽쉿슁슈슉슐슘슛슝스슥슨슬슭슴습슷승시식신싣실싫심십싯싱싶싸싹싻싼쌀쌈쌉쌌쌍쌓쌔쌕쌘쌜쌤쌥쌨쌩썅써썩썬썰썲썸썹썼썽쎄쎈쎌쏀쏘쏙쏜쏟쏠쏢쏨쏩쏭쏴쏵쏸쐈쐐쐤쐬쐰쐴쐼쐽쑈쑤쑥쑨쑬쑴쑵쑹쒀쒔쒜쒸쒼쓩쓰쓱쓴쓸쓺쓿씀씁씌씐씔씜씨씩씬씰씸씹씻씽아악안앉않알앍앎앓암압앗았앙앝앞애액앤앨앰앱앳앴앵야약얀얄얇얌얍얏양얕얗얘얜얠얩어억언얹얻얼얽얾엄업없엇었엉엊엌엎에엑엔엘엠엡엣엥여역엮연열엶엷염엽엾엿였영옅옆옇예옌옐옘옙옛옜오옥온올옭옮옰옳옴옵옷옹옻와왁완왈왐왑왓왔왕왜왝왠왬왯왱외왹왼욀욈욉욋욍요욕욘욜욤욥욧용우욱운울욹욺움웁웃웅워웍원월웜웝웠웡웨웩웬웰웸웹웽위윅윈윌윔윕윗윙유육윤율윰윱윳융윷으윽은을읊음읍읏응읒읓읔읕읖읗의읜읠읨읫이익인일읽읾잃임입잇있잉잊잎자작잔잖잗잘잚잠잡잣잤장잦재잭잰잴잼잽잿쟀쟁쟈쟉쟌쟎쟐쟘쟝쟤쟨쟬저적전절젊점접젓정젖제젝젠젤젬젭젯젱져젼졀졈졉졌졍졔조족존졸졺좀좁좃종좆좇좋좌좍좔좝좟좡좨좼좽죄죈죌죔죕죗죙죠죡죤죵주죽준줄줅줆줌줍줏중줘줬줴쥐쥑쥔쥘쥠쥡쥣쥬쥰쥴쥼즈즉즌즐즘즙즛증지직진짇질짊짐집짓징짖짙짚짜짝짠짢짤짧짬짭짯짰짱째짹짼쨀쨈쨉쨋쨌쨍쨔쨘쨩쩌쩍쩐쩔쩜쩝쩟쩠쩡쩨쩽쪄쪘쪼쪽쫀쫄쫌쫍쫏쫑쫓쫘쫙쫠쫬쫴쬈쬐쬔쬘쬠쬡쭁쭈쭉쭌쭐쭘쭙쭝쭤쭸쭹쮜쮸쯔쯤쯧쯩찌찍찐찔찜찝찡찢찧차착찬찮찰참찹찻찼창찾채책챈챌챔챕챗챘챙챠챤챦챨챰챵처척천철첨첩첫첬청체첵첸첼쳄쳅쳇쳉쳐쳔쳤쳬쳰촁초촉촌촐촘촙촛총촤촨촬촹최쵠쵤쵬쵭쵯쵱쵸춈추축춘출춤춥춧충춰췄췌췐취췬췰췸췹췻췽츄츈츌츔츙츠측츤츨츰츱츳층치칙친칟칠칡침칩칫칭카칵칸칼캄캅캇캉캐캑캔캘캠캡캣캤캥캬캭컁커컥컨컫컬컴컵컷컸컹케켁켄켈켐켑켓켕켜켠켤켬켭켯켰켱켸코콕콘콜콤콥콧콩콰콱콴콸쾀쾅쾌쾡쾨쾰쿄쿠쿡쿤쿨쿰쿱쿳쿵쿼퀀퀄퀑퀘퀭퀴퀵퀸퀼큄큅큇큉큐큔큘큠크큭큰클큼큽킁키킥킨킬킴킵킷킹타탁탄탈탉탐탑탓탔탕태택탠탤탬탭탯탰탱탸턍터턱턴털턺텀텁텃텄텅테텍텐텔템텝텟텡텨텬텼톄톈토톡톤톨톰톱톳통톺톼퇀퇘퇴퇸툇툉툐투툭툰툴툼툽툿퉁퉈퉜퉤튀튁튄튈튐튑튕튜튠튤튬튱트특튼튿틀틂틈틉틋틔틘틜틤틥티틱틴틸팀팁팃팅파팦팍팎판팔팖팜팝팟팠팡팥패팩팬팰팸팹팻팼팽퍄퍅퍼퍽펀펄펌펍펏펐펑페펙펜펠펨펩펫펭펴편펼폄폅폈평폐폘폡폣포폭폰폴폼폽폿퐁퐈퐝푀푄표푠푤푭푯푸푹푼푿풀풂품풉풋풍풔풩퓌퓐퓔퓜퓟퓨퓬퓰퓸퓻퓽프픈플픔픕픗피픽핀필핌핍핏핑하학한할핥함합핫항해핵핸핼햄햅햇했행햐향허헉헌헐헒험헙헛헝헤헥헨헬헴헵헷헹혀혁현혈혐협혓혔형혜혠혤혭호혹혼홀홅홈홉홋홍홑화확환활홧황홰홱홴횃횅회획횐횔횝횟횡효횬횰횹횻후훅훈훌훑훔훗훙훠훤훨훰훵훼훽휀휄휑휘휙휜휠휨휩휫휭휴휵휸휼흄흇흉흐흑흔흖흗흘흙흠흡흣흥흩희흰흴흼흽힁히힉힌힐힘힙힛힝!@#$%^&*《》()[]【】【】\"\'◐◑oㅇ⊙○◎◉◀▶⇒◆■□△※☎☏;:/.?<>-_=+×\￦|₩~,.㎡㎥ℓ㎖㎘→「」『』·ㆍ1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ읩①②③④⑤月日軍 ")
        

    def CreateDataset(self, nums, moveTxt = [0,0], txtFont = "malgun.ttf", txtSize = 10, debug = False):
        """
        Dataset을 만든다.

        Args:
        ---
        `nums [int]` : 생성할 이미지 갯수

        `moveTxt [int, int]` : 빈칸 고정 위치 이동

        `txtFont [string]` : 글씨체

        `txtSize [int]` : 글자 크기

        `debug [bool]` : 디버그용(라인 표시)

        Returns:
        ---
        None

        """
        st = time.time()
        
        print()
        print('Create data')
        for i in tqdm(range(nums)):
            data_list = self.createData()
            
            if moveTxt[0] ==0 and moveTxt[1] == 0:
                result_img, result_json  = self.createImg(data_list, moveTxt, txtFont, txtSize, debug)
            else:
                move_x = random.randint(-moveTxt[0],moveTxt[0])
                move_y = random.randint(-moveTxt[1],moveTxt[1])
                result_img, result_json  = self.createImg(data_list, [move_x, move_y], txtFont, txtSize, debug)

            if debug:
                cv2.namedWindow("result", cv2.WINDOW_NORMAL)
                cv2.imshow('result', result_img)
                cv2.waitKey()
                cv2.destroyAllWindows()
        
            with open(self.saveJsonPath + rf'\{i}.json', 'w', encoding='utf-8') as file:
                file.write(result_json)
                if debug:
                    print(result_json)
            
            cv2.imwrite(self.saveIMGPath + rf'\{i}.jpg', result_img)

        et = time.time()
        elapsed_time = et - st
        print(f'Execution time: {elapsed_time:.4f} seconds')

    def createData(self):
        data_list = []
        # 의약품
        data_list += self.createMedicineOrInjection(type=0)
        
        # 주사
        data_list += self.createMedicineOrInjection(type=1)

        # 용법
        data_list.append(self.crateIDdata(id = 82, valueType=1))
        
        # 참고사항
        data_list.append(self.crateIDdata(id = 113, valueType=1))


        id = random.randint(24,28)
        if id == 28:
            # 체크를 하고 29에 글자 삽입
            mask = self.position_df['id'] == id
            data_list.append(["■", self.position_df[mask][['x1', 'y1']].values[0]])
            
            # 글자 삽입
            mask = self.position_df['id'] == 29
            #일단, A
            data_list.append(["A", self.position_df[mask][['x1', 'y1']].values[0]])

        else:
            # 체크  
            mask = self.position_df['id'] == id
            data_list.append(["■", self.position_df[mask][['x1', 'y1']].values[0]])
            
        id = random.randint(83,84)
        mask = self.position_df['id'] == id
        data_list.append(["■", self.position_df[mask][['x1', 'y1']].values[0]])


        # id 0~4
        data_list.append(self.crateIDdata(id = 0, valueType=0, intRange=[10000000, 12000000]))
        data_list.append(self.crateIDdata(id = 1, valueType=0, intRange=[2000, 2100]))
        data_list.append(self.crateIDdata(id = 2, valueType=0, intRange=[1, 12]))
        data_list.append(self.crateIDdata(id = 3, valueType=0, intRange=[1, 31]))
        data_list.append(self.crateIDdata(id = 4, valueType=0, intRange=[1, 10000]))

        #이름 생성
        data_list.append(self.name_maker(id=5))
        data_list.append(self.name_maker(id=21))
        data_list.append(self.name_maker(id=116))
        data_list.append(self.name_maker(id=117))

        # id 6~10
        data_list.append(self.crateIDdata(id = 6, valueType=2))
        data_list.append(self.crateIDdata(id = 7, valueType=1))
        data_list.append(self.crateIDdata(id = 8, valueType=3))
        data_list.append(self.crateIDdata(id = 9, valueType=3))
        data_list.append(self.crateIDdata(id = 10, valueType=4))

        # id 11 ~ 21
        # for i in range(11,21):  
        #     data_list.append(self.kcd(i))
        data_list += self.kcd_generator(11)
        temp_ = random.randint(0,2)
        if temp_ ==1 :
            data_list += self.kcd_generator(16)

        # id 22~23, 114~115, 118~120
        data_list.append(self.crateIDdata(id = 22, valueType=5))
        data_list.append(self.crateIDdata(id = 23, valueType=0, intRange=[100000, 999999]))
        data_list.append(self.crateIDdata(id = 114, valueType=0, intRange=[1, 366]))
        data_list.append(self.crateIDdata(id = 115, valueType=1))

        data_list.append(self.crateIDdata(id = 118, valueType=0, intRange=[1, 99]))
        data_list.append(self.crateIDdata(id = 119, valueType=6, intRange=[100000, 999999]))

        data_list.append(self.crateIDdata(id = 120, valueType=1))

        return data_list


    def createMedicineOrInjection(self, type):
        """
        의약품 또는 주사 데이터를 만든다.

        Args:
        ---
        `type [int]` : 0 = 의약품, 1 = 주사

        Returns:
        ---
        
        data_list

        """
        maxCNT = 13
        setid = 30
        sumid = 13

        # 주사 세팅
        if type == 1:
            maxCNT = 7
            setid = 85
            sumid = 7

        data_list = []
        cnt = random.randint(1, maxCNT)
        for i in range(cnt):
            index = random.randint(0, 40000) 
            namesize = random.randint(4, 20)
            medi_name = self.medicine_df.iloc[index, 2][:namesize]
            medi_name = re.sub("\n", "", medi_name)
            medi_name = re.sub("\r", "", medi_name)
            medi_name = ''.join([char for char in medi_name if char in self.kor])

            amount = random.randint(1, 10) # 1회 투약량
            count = random.randint(1, 10) # 1회 투약횟수
            duration =  random.randint(1, 14) # 총 투약일수

            id = setid + i
            position = []
            for j in range(4):
                id_ = id + j * sumid
                mask = self.position_df['id'] == id_
                position.append(self.position_df[mask][['x1', 'y1']].values[0])
            

            data_list.append([medi_name, position[0]])
            data_list.append([str(amount), position[1]])
            data_list.append([str(count), position[2]])
            data_list.append([str(duration), position[3]])

        return data_list
    
    def crateIDdata(self, id, valueType = 0, strRange = [0,40000], intRange = [0,40000]):
        """
        id에 해당하는 값을 생성한다.

        Args:
        ---
        `id [int]` : id

        `valueType [int]` : 0 = int, 1 = str, 2 =  f'{year}{month}{day}-{gender}{random_number}', 3 = phoneNum, 4 = email, 5 = 의사 종류
                            6 = {year}{month}{day}

        `strRange [min, max]` : str value 범위

        `intRange [min, max]` : int value 범위

        Returns:
        ---
                
        data list

        """
        


        # value
        val = random.randint(intRange[0], intRange[1])
        if valueType == 1:
            # 의약품 이름 중 가져오기
            index = random.randint(0, 40000)
            namesize = random.randint(4, 15)
            val = self.medicine_df.iloc[index, 2][:namesize]
            val = re.sub('\n','',val)
            val = re.sub('\r','',val)
            val = ''.join([char for char in val if char in self.kor])
        elif valueType == 2:
            # 날짜생성
            year_full=str(random.randint(1950,2023))
            year=year_full[2:4]       
            month=str(random.randint(1,13)).zfill(2)        
            day=str(random.randint(1,32))    

            gender=random.randint(1,2) if year_full[0:2]=='19' else random.randint(3,4)   
            random_number=str(random.randint(0,999999)).zfill(6)
            val = f'{year}{month}{day}-{gender}{random_number}'

        elif valueType == 3:
            # 전화번호
            area_code_list=['02','032','042','051','052','053','062','064','031','033','041','043','054','055','061','063','010']
            area_code_idx=random.randint(0,len(area_code_list) - 1)
            area_code=area_code_list[area_code_idx]
            
            phone_number1=str(random.randint(0,9999)).zfill(4)
            phone_number2=str(random.randint(0,9999)).zfill(4)
            val = f'{area_code}-{phone_number1}-{phone_number2}'

        elif valueType == 4:
            string='abcdefghijklmnopqrstuvwxyz'
            string_list=list(string)

            id_list=string_list.copy()
            random.shuffle(id_list)

            id_length=random.randint(6,12+1)
            id_=''.join(id_list[:id_length])

            email_idx=random.randint(0,2)
            email_list=['@gmail.com','@naver.com','@daum.net']
            email=email_list[email_idx]
            val = f'{id_}{email}'
        elif valueType == 5:
            license_list = ["의사", "치과의사", "한의사"]
            n = random.randint(0,2)
            val = license_list[n]
        elif valueType == 6:
            year_full=str(random.randint(1950,2023))            
            year=year_full[2:4]        
            month=str(random.randint(1,13)).zfill(2)        
            day=str(random.randint(1,32)).zfill(2)  
            val = f'{year}년 {month}월 {day}일'

        
        # id에 해당하는 위치
        mask = self.position_df['id'] == id
        position = self.position_df[mask][['x1', 'y1']].values[0]

        return [str(val), position]
    
    def name_maker(self,id):
        """
        id에 해당하는 이름을 생성

        Args:
        ---

        `id [int]` : id

        Returns:
        ---
        
        data list

        """
        data_list = []
        last_name=['김', '이', '박', '최', '정', '강', '조', '윤', '장', '임', '한', '오', '서', '신', '권', '황', '안', '송', '류', '전', '홍', '고', '문', '양', '손', '배', '조', '백', '허', '유', '남', '심', '노', '정', '하', '곽', '성', '차', '주', '우', '구', '신', '임', '라', '전', '민', '유', '진', '지', '엄', '채', '원', '천', '방', '공', '강', '현', '함', '변', '염', '양', '변', '여', '추', '노', '도', '소', '신', '석', '선', '설', '마', '길', '주', '연', '방', '위', '표', '명', '기', '반', '왕', '금', '옥', '육', '인', '맹', '제', '모', '장', '남궁', '탁', '국', '여', '진', '어', '은', '편', '구', '용', '유', '예', '경', '봉', '정', '석', '사', '부', '황보', '가', '복', '태', '목', '진', '형', '계', '최', '피', '두', '지', '감', '장']
        first_name=['서율', '하영', '서은', '도희', '도윤', '서윤', '서준', '은우', '시아', '하진', '다인', '예서', '민재', '시은', '주은', '은서', '시현', '시원', '하늘', '하람', '도영', '은호', '서아', '민규', '예원', '서진', '서영', '지민', '지우', '민하', '은준', '민주', '민서', '윤아', '다연', '주희', '다온', '다원', '은정', '윤재', '예은', '서하', '지현', '민지', '민영', '하은', '승현', '서우', '민혁', '현서', '승주', '시우', '승우', '수아', '수민', '시윤', '지원', '승민', '다은', '주현', '현준', '예빈', '은주', '도현', '지안', '지유', '혜원', '유진', '지아', '민아', '주원', '예준', '지윤', '하윤', '지애', '채원', '예진', '지후', '예나', '진아', '진서', '진우', '소율', '지호', '우진', '정우', '소윤', '재민', '건우', '윤서', '윤호', '수빈','하율','예린','현우','준우','다현','서연','연우','하린','유준','하준','준서','이준','서현','은지','민준','선우','서율', '하영', '서은', '도희', '도윤', '서윤', '서준', '은우', '시아', '하진', '다인', '예서', '민재', '시은']

        i=random.randint(0,len(last_name)-1)
        j=random.randint(0,len(first_name) -1)
        val = f'{last_name[i]}{first_name[j]}'

        # id에 해당하는 위치
        mask = self.position_df['id'] == id
        position = self.position_df[mask][['x1', 'y1']].values[0]

        return [str(val), position]
    
    def kcd_generator(self,id = 11):
        alphabet_list=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        alphabet_idx=random.randint(0,len(alphabet_list)-1)
        alphabet=alphabet_list[alphabet_idx]        

        kcd_list=[]
        mask = self.position_df['id'] == id
        position = self.position_df[mask][['x1', 'y1']].values[0]
        kcd_list.append([alphabet,position])

        num=random.randint(1,4)
        for n in range(num):
            id += 1
            number=random.randint(1,9)     
            mask = self.position_df['id'] == id
            position = self.position_df[mask][['x1', 'y1']].values[0]
            kcd_list.append([str(number),position])            

        return kcd_list

    
    # def kcd(self,id):
    #     string='abcdefghijklmnopqrstuvwxyz'
    #     string_list=list(string.upper())
    #     kcd_list=string_list.copy()
        
    #     random.shuffle(kcd_list)
        
    #     kcd_num=str(random.randint(0,9))

    #      # id에 해당하는 위치
    #     mask = self.position_df['id'] == id
    #     position = self.position_df[mask][['x1', 'y1']].values[0]

    #     return [kcd_list[0]+kcd_num,position]
    

    def createImg(self, data, moveTxt = [0,0], txtFont = "malgun.ttf", txtSize = 15, debug=False):
        imgRGB = cv2.cvtColor(self.prescription_img, cv2.COLOR_BGR2RGB)

        font = ImageFont.truetype(txtFont, txtSize)

        # 이미지를 PIL Image 객체로 변환
        img = Image.fromarray(imgRGB)

        # Draw 객체 생성
        draw = ImageDraw.Draw(img)


        text_sizes_list = []
        # 텍스트를 추가하는 for loop    
        for text, position in data:
            # .text(위치, 텍스트, 텍스트 색, 폰트)
            text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:4]

            position[0] += moveTxt[0] + 10
            position[1] += moveTxt[1]

            x = position[0]  + text_width / 2
            y = position[1]  + text_height / 2
            
            # Calculate the y position to center the text
            draw.text((x, y), text, (0, 0, 0), font=font,anchor='mm')
            
            text_sizes_list.append([position[0], position[1], position[0] + text_width, position[1] + text_height, text])
            

        # PIL Image를 다시 numpy 배열로 변환
        img_with_text = np.array(img)
        result_img = cv2.cvtColor(img_with_text, cv2.COLOR_RGB2BGR)
        
        #사각형 그리기
        if debug:
            for x1, y1, x2, y2, txt in text_sizes_list:
                cv2.rectangle(result_img, (x1, y1), (x2, y2), (0, 255, 0), 1)



        # 처방전 라벨링 사각형 그리기
        # 'id', 'x1', 'y1', 'y2' 컬럼의 값을 이용해서 텍스트와 좌표값을 가진 딕셔너리 생성
        position_list = [[row['id'], row['x1'] + moveTxt[0], row['y1'] + moveTxt[1] ,row['x2'] + moveTxt[0] , row['y2'] + moveTxt[1], row['cont']] for _, row in self.labeling_df.iterrows()]

        
        #사각형 그리기
        if debug:
            for id, x1, y1, x2, y2, txt in position_list:
                cv2.rectangle(result_img, (x1, y1), (x2, y2), (0, 255, 0), 1)
                text_sizes_list.append([x1, y1, x2, y2,txt])

        # Json 파일 만들기
        text_sizes_dics = []
        for x1, y1, x2, y2, txt in text_sizes_list:
            text_sizes_dics.append({'x1' : int(x1), 'y1' : int(y1), 'x2' : int(x2), 'y2' : int(y2), 'txt' : str(txt)})
        
        for index, row in self.labeling_df.iterrows():
            text_sizes_dics.append({'x1' : int(row['x1']), 'y1' : int(row['y1']), 'x2' : int(row['x2']), 'y2' : int(row['y2']), 'txt' : str(row['cont'])})

        result_json = json.dumps(text_sizes_dics, ensure_ascii=False , indent=4)


        return result_img, result_json

    def convertDataSetForResnet(self):
        print('\nconvertDataSetForResnet')
        st = time.time()
        dataSetIMG_list = glob.glob(fr"{self.saveIMGPath}\*.jpg")
        dataSetJson_list = glob.glob(fr"{self.saveJsonPath}\*.json")
        
        dataSetIMG_list = natsorted(dataSetIMG_list)
        dataSetJson_list = natsorted(dataSetJson_list)
        
        txt_content = ""
        for imgPath, jsonPath in tqdm(zip(dataSetIMG_list, dataSetJson_list),total=len(dataSetIMG_list)):
            # 이미지 자르기(각 이미지별로 Json을 읽어서 글자별로 자르기)
            ## 이미지 읽기
            img = cv2.imread(imgPath)
            imgname = os.path.splitext(os.path.basename(imgPath))[0]
            
            
            #Json 읽기
            json = pd.read_json(jsonPath)
            cnt = 0
            
            
            for _, row in json.iterrows():
                x1 = row['x1']
                x2 = row['x2']
                y1 = row['y1']
                y2 = row['y2']
                content = row['txt']
                imgPath_ = f'{self.savepathConvertIMG_Resnet}\{imgname}_{cnt}.jpg'
                cv2.imwrite(imgPath_, img[y1:y2, x1:x2])
                
                txt_content += f'{imgname}_{cnt}.jpg\t{content}\n'
                cnt+=1
                        
                        
        with open(f'{self.savepathConvertLBL_Resnet}\lable.txt', 'w', encoding='utf-8') as f:
                f.write(txt_content)
        
        et = time.time()
        elapsed_time = et - st
        print(f'Execution time: {elapsed_time:.4f} seconds')



def makePath(path):
       
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)
    else:
        shutil.rmtree(path)
        os.makedirs(path, exist_ok=True)
        



dbPath = r'1.data\3.DB\db.csv'
medicinePath = r'1.data\3.DB\medicine_list.csv'
labelingPath = r'1.data\3.DB\prescript_labeling(Fix).json'
imgPath = r'1.data\1.img\prescription.png'


        
saveIMGPath = r'1.data\4.dataSet\img'
saveJsonPath = r'1.data\4.dataSet\json'
savepathConvertIMG_Resnet = r'1.data\4.dataSet\Resnet\img'
savepathConvertLBL_Resnet = r'1.data\4.dataSet\Resnet\label'  

makePath(saveIMGPath)
makePath(saveJsonPath)
makePath(savepathConvertIMG_Resnet)
makePath(savepathConvertLBL_Resnet)



dataset =  DataSet(saveIMGPath= saveIMGPath,savepathConvertIMG_Resnet= savepathConvertIMG_Resnet,savepathConvertLBL_Resnet = savepathConvertLBL_Resnet, saveJsonPath = saveJsonPath, dbPath = dbPath, medicinePath = medicinePath, labelingPath = labelingPath, imgPath=imgPath)

nums = 10000
debug = False
moveTxt = [10, 8]
dataset.CreateDataset(nums=nums, moveTxt = moveTxt, debug=debug)
dataset.convertDataSetForResnet()


saveIMGPath = r'1.data\4.dataSet\img2'
saveJsonPath = r'1.data\4.dataSet\json2'
savepathConvertIMG_Resnet = r'1.data\4.dataSet\Resnet\img2'
savepathConvertLBL_Resnet = r'1.data\4.dataSet\Resnet\label2'  

makePath(saveIMGPath)
makePath(saveJsonPath)
makePath(savepathConvertIMG_Resnet)
makePath(savepathConvertLBL_Resnet)



dataset =  DataSet(saveIMGPath= saveIMGPath,savepathConvertIMG_Resnet= savepathConvertIMG_Resnet,savepathConvertLBL_Resnet = savepathConvertLBL_Resnet, saveJsonPath = saveJsonPath, dbPath = dbPath, medicinePath = medicinePath, labelingPath = labelingPath, imgPath=imgPath)

nums = 10000
debug = False
moveTxt = [10, 8]
dataset.CreateDataset(nums=nums, moveTxt = moveTxt, debug=debug)
dataset.convertDataSetForResnet()

saveIMGPath = r'1.data\4.dataSet\img3'
saveJsonPath = r'1.data\4.dataSet\json3'
savepathConvertIMG_Resnet = r'1.data\4.dataSet\Resnet\img3'
savepathConvertLBL_Resnet = r'1.data\4.dataSet\Resnet\label3'  

makePath(saveIMGPath)
makePath(saveJsonPath)
makePath(savepathConvertIMG_Resnet)
makePath(savepathConvertLBL_Resnet)



dataset =  DataSet(saveIMGPath= saveIMGPath,savepathConvertIMG_Resnet= savepathConvertIMG_Resnet,savepathConvertLBL_Resnet = savepathConvertLBL_Resnet, saveJsonPath = saveJsonPath, dbPath = dbPath, medicinePath = medicinePath, labelingPath = labelingPath, imgPath=imgPath)

nums = 10000
debug = False
moveTxt = [10, 8]
dataset.CreateDataset(nums=nums, moveTxt = moveTxt, debug=debug)
dataset.convertDataSetForResnet()

saveIMGPath = r'1.data\4.dataSet\img4'
saveJsonPath = r'1.data\4.dataSet\json4'
savepathConvertIMG_Resnet = r'1.data\4.dataSet\Resnet\img4'
savepathConvertLBL_Resnet = r'1.data\4.dataSet\Resnet\label4'  

makePath(saveIMGPath)
makePath(saveJsonPath)
makePath(savepathConvertIMG_Resnet)
makePath(savepathConvertLBL_Resnet)



dataset =  DataSet(saveIMGPath= saveIMGPath,savepathConvertIMG_Resnet= savepathConvertIMG_Resnet,savepathConvertLBL_Resnet = savepathConvertLBL_Resnet, saveJsonPath = saveJsonPath, dbPath = dbPath, medicinePath = medicinePath, labelingPath = labelingPath, imgPath=imgPath)

nums = 10000
debug = False
moveTxt = [10, 8]
dataset.CreateDataset(nums=nums, moveTxt = moveTxt, debug=debug)
dataset.convertDataSetForResnet()