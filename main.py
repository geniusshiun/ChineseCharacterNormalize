# -*- coding: UTF-8 -*-
from functools import reduce
from multiprocessing import Pool, cpu_count
import operator
import sys, re, time, os
from CNtool import hantoutf32,utf32toutf16
import json
#from utils import humansize, humantime, processbar
def strQ2B(ustring):
    """把字串全形轉半形"""
    rstring = []
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code==0x3000:
            inside_code=0x0020
        else:
            if (inside_code-0xfee0 > 0):
                inside_code-=0xfee0

        if inside_code<0x0020 or inside_code>0x7e:   #轉完之後不是半形字元返回原來的字元
            rstring.append(uchar)
        else:
            rstring.append(chr(inside_code))

    return ''.join(rstring)
def strNormalize(data):
    from CNtool import hantoutf32,utf32toutf16
    import re
    import json
    _transferSymbol_non = []
    tradition = '廠幾兒虧與萬億個勺麼廣門義屍衛飛習馬鄉豐開無專扎藝廳區歷車岡貝見氣長僕幣僅從倉風勻烏鳳為憶訂計認隊辦勸書擊撲節術厲龍滅軋東業舊帥歸葉電號叨嘆們儀叢樂處鳥務飢閃蘭匯頭漢寧討寫讓禮訓議訊記遼邊發聖對糾絲動執鞏擴掃揚場亞朴機權過協壓厭頁奪達夾軌邁畢貞師塵當嚇蟲團嗎嶼歲豈剛則網遷喬偉傳優傷價華偽會殺眾爺傘創肌雜負壯沖莊慶劉齊產決閉問闖並關湯興講軍許論農諷設訪尋迅盡導異孫陣陽階陰婦媽戲觀歡買紅纖級約紀馳壽麥進遠違運撫壇壞擾壩貢搶墳坊護殼塊聲報蒼嚴蘆勞蘇極楊兩麗醫辰勵還殲來連堅時吳縣園曠圍噸郵員聽嗚崗帳財針釘亂體伶徹余鄰腸龜猶條飯飲凍狀畝況庫療應這棄冶閒間悶灶燦沃溝懷憂窮災證啟評補識訴診詞譯靈層遲張際陸陳勁雞驅純紗納綱駁縱紛紙紋紡驢紐環責現規攏揀擔頂擁勢攔撥擇蘋莖櫃槍構傑喪畫棗賣礦碼廁奮態歐壟轟頃轉斬輪軟齒虜腎賢國暢鳴詠羅幟嶺凱敗販購圖釣偵側憑僑貨質徑貪貧膚腫脹脅魚備飾飽飼變廟劑廢淨閘鬧鄭單爐淺淚瀉潑澤憐學寶審簾實試詩誠襯視話誕詢該詳肅錄隸屆陝限駕參艱線練組細駛織終駐駝紹經貫幫掛項撓趙擋墊擠揮薦帶繭蕩榮藥標棟欄樹咸磚砌牽殘輕鴉戰點臨覽豎削嘗顯啞貴蝦蟻螞雖罵嘩響峽罰賤鈔鐘鋼鑰鉤選適種復倆貸順儉須劍膽勝脈狹獅獨獄貿饒蝕餃餅彎將獎瘡瘋親聞閥閣養類逆總煉爛潔灑澆濁測濟渾濃惱舉覺憲竊語襖誤誘說誦墾晝險嬌賀壘綁絨結繞驕繪給絡駱絕絞統豔蠶頑撈載趕鹽損撿換熱恐壺蓮獲惡檔橋礎顧轎較頓斃慮監緊黨曬曉暈喚罷圓賊賄錢鉗鑽鐵鈴鉛犧敵積稱筆筍債傾艦艙愛頌胳髒膠腦皺餓戀槳漿離資閱煩燒燭遞濤澇潤漲燙湧寬賓請諸讀襪課誰調諒談誼剝懇劇難預絹驗繼掠職蘿營夢檢聾襲輔輛虛懸嶄銅鏟銀籠償銜盤鴿領臉獵餡館癢蓋斷獸漸漁滲慚驚慘慣窯謀謊禍謎彈隱嬸頸績緒續騎繩維綿綢綠趨擱摟攪聯確暫輩輝賞噴踐遺賭賠鑄鋪鏈銷鎖鋤鍋鏽鋒銳筐築篩儲懲釋臘魯饞蠻闊糞濕灣憤竄窩褲謝謠謙屬屢緞緩編騙緣攝擺攤鵲藍獻樓賴霧輸齡鑑錯錫鑼錘錦鍵鋸矮辭籌簽簡騰觸醬糧數滿濾濫滾濱灘譽謹縫纏牆願顆蠟蠅賺鍬鍛穩籮饅賽譜騾縮囑鎮顏額聰櫻飄瞞題顛贈鏡贊籃辯懶繳辮驟鐮侖譏鄧盧嘰爾馮迂籲吆倫鳧妝汛諱訝訛訟訣馱馴紉瑪韌摳掄塢擬蕪葦杈軒鹵嘔嗆嶇佃狽鳩廬閏兌瀝淪洶滄滬詛詐墜緯坯樞楓礬毆曇嚨賬貶貯俠僥劊覓龐瘧濘寵詭屜彌參紳駒絆繹貳挾莢蕎薺葷熒棧硯鷗軸勳喲鈣鈍鈉欽鈞鈕氫朧餌巒颯閨閩婁爍炫窪誡誣誨遜隕駭摯搗聶荸萊瑩鶯棲樺樁賈礫嘮鴦贓鉀鉚秫賃聳頒臍膿鴕鴛餒齋渦渙滌澗澀憫竅諾誹諄駿瑣麩擲撣摻螢蕭薩醞碩顱晤囉嘯邏銬鐺鋁鍘銑銘矯秸穢軀斂閻闡煥鴻淵諜諧襠袱禱謁謂諺頗綽繃綜綻綴瓊攬攙蔣韓頰靂翹鑿喳晾疇鵑賦贖賜銼鋅牘憊瘓滯潰濺謗緬纜締縷騷鵡欖輻輯頻蹺錨錐鍁錠錳頹膩鵬雛饃餾稟痺謄寢褂裸謬繽贅蔫藹鹼轅轄蟬鍍簫輿譚纓攆鑷鎬簍鯉癟癱瀾譴鶴繚轍鸚籬鯨瀕韁贍鐐鱷囂鰭癩攢鬢躪鑲'
    simple = '厂几儿亏与万亿个勺么广门义尸卫飞习马乡丰开无专扎艺厅区历车冈贝见气长仆币仅从仓风匀乌凤为忆订计认队办劝书击扑节术厉龙灭轧东业旧帅归叶电号叨叹们仪丛乐处鸟务饥闪兰汇头汉宁讨写让礼训议讯记辽边发圣对纠丝动执巩扩扫扬场亚朴机权过协压厌页夺达夹轨迈毕贞师尘当吓虫团吗屿岁岂刚则网迁乔伟传优伤价华伪会杀众爷伞创肌杂负壮冲庄庆刘齐产决闭问闯并关汤兴讲军许论农讽设访寻迅尽导异孙阵阳阶阴妇妈戏观欢买红纤级约纪驰寿麦进远违运抚坛坏扰坝贡抢坟坊护壳块声报苍严芦劳苏极杨两丽医辰励还歼来连坚时吴县园旷围吨邮员听呜岗帐财针钉乱体伶彻余邻肠龟犹条饭饮冻状亩况库疗应这弃冶闲间闷灶灿沃沟怀忧穷灾证启评补识诉诊词译灵层迟张际陆陈劲鸡驱纯纱纳纲驳纵纷纸纹纺驴纽环责现规拢拣担顶拥势拦拨择苹茎柜枪构杰丧画枣卖矿码厕奋态欧垄轰顷转斩轮软齿虏肾贤国畅鸣咏罗帜岭凯败贩购图钓侦侧凭侨货质径贪贫肤肿胀胁鱼备饰饱饲变庙剂废净闸闹郑单炉浅泪泻泼泽怜学宝审帘实试诗诚衬视话诞询该详肃录隶届陕限驾参艰线练组细驶织终驻驼绍经贯帮挂项挠赵挡垫挤挥荐带茧荡荣药标栋栏树咸砖砌牵残轻鸦战点临览竖削尝显哑贵虾蚁蚂虽骂哗响峡罚贱钞钟钢钥钩选适种复俩贷顺俭须剑胆胜脉狭狮独狱贸饶蚀饺饼弯将奖疮疯亲闻阀阁养类逆总炼烂洁洒浇浊测济浑浓恼举觉宪窃语袄误诱说诵垦昼险娇贺垒绑绒结绕骄绘给络骆绝绞统艳蚕顽捞载赶盐损捡换热恐壶莲获恶档桥础顾轿较顿毙虑监紧党晒晓晕唤罢圆贼贿钱钳钻铁铃铅牺敌积称笔笋债倾舰舱爱颂胳脏胶脑皱饿恋桨浆离资阅烦烧烛递涛涝润涨烫涌宽宾请诸读袜课谁调谅谈谊剥恳剧难预绢验继掠职萝营梦检聋袭辅辆虚悬崭铜铲银笼偿衔盘鸽领脸猎馅馆痒盖断兽渐渔渗惭惊惨惯窑谋谎祸谜弹隐婶颈绩绪续骑绳维绵绸绿趋搁搂搅联确暂辈辉赏喷践遗赌赔铸铺链销锁锄锅锈锋锐筐筑筛储惩释腊鲁馋蛮阔粪湿湾愤窜窝裤谢谣谦属屡缎缓编骗缘摄摆摊鹊蓝献楼赖雾输龄鉴错锡锣锤锦键锯矮辞筹签简腾触酱粮数满滤滥滚滨滩誉谨缝缠墙愿颗蜡蝇赚锹锻稳箩馒赛谱骡缩嘱镇颜额聪樱飘瞒题颠赠镜赞篮辩懒缴辫骤镰仑讥邓卢叽尔冯迂吁吆伦凫妆汛讳讶讹讼诀驮驯纫玛韧抠抡坞拟芜苇杈轩卤呕呛岖佃狈鸠庐闰兑沥沦汹沧沪诅诈坠纬坯枢枫矾殴昙咙账贬贮侠侥刽觅庞疟泞宠诡屉弥叁绅驹绊绎贰挟荚荞荠荤荧栈砚鸥轴勋哟钙钝钠钦钧钮氢胧饵峦飒闺闽娄烁炫洼诫诬诲逊陨骇挚捣聂荸莱莹莺栖桦桩贾砾唠鸯赃钾铆秫赁耸颁脐脓鸵鸳馁斋涡涣涤涧涩悯窍诺诽谆骏琐麸掷掸掺萤萧萨酝硕颅晤啰啸逻铐铛铝铡铣铭矫秸秽躯敛阎阐焕鸿渊谍谐裆袱祷谒谓谚颇绰绷综绽缀琼揽搀蒋韩颊雳翘凿喳晾畴鹃赋赎赐锉锌牍惫痪滞溃溅谤缅缆缔缕骚鹉榄辐辑频跷锚锥锨锭锰颓腻鹏雏馍馏禀痹誊寝褂裸谬缤赘蔫蔼碱辕辖蝉镀箫舆谭缨撵镊镐篓鲤瘪瘫澜谴鹤缭辙鹦篱鲸濒缰赡镣鳄嚣鳍癞攒鬓躏镶'
    s2t = {}
    for index in range(len(tradition)):
        s2t[simple[index]] = tradition[index]
    specialmapping = {'•':'§','╳':'§'}
    totalmapping = {}
    with open('hanMappingTable.txt','r',encoding='utf8') as f:
        totalmapping = json.loads(''.join(f.readlines()))
    spaceIndex = [m.start() for m in re.finditer('(\s)',data)]
    data = str(data).replace(' ','')
    
    chiIndexList = [m.start() for m in re.finditer('([一-龥]+)',data)]
    chiList = re.findall('([一-龥]+)',data)
    nonchiIndexList = [m.start() for m in re.finditer('([^一-龥]+)',data)]
    nonchiList = [item for item in re.sub('([一-龥]+)',' ',data).split(' ') if not item == '']
    #print(chiList,chiIndexList,nonchiList,nonchiIndexList)
    transferdataDict = {}
    
    while chiList:
        #print(chiIndexList)
        contiChi = chiList[0]
        transferdata = []
        for w in contiChi:
            
            if w in s2t:
                #STtransfer.append(w)
                transferdata.append(s2t[w])
                #print(w)
            else:
                index = hantoutf32(w)
                try:
                    index16 = utf32toutf16(index)[3:-1].upper()
                    #print(index16)
                except:
                    print('check',w)
                    continue
                if index16 in totalmapping:
                    mappinghan = json.loads(utf32toutf16(totalmapping[index16]))
                    transferdata.append(mappinghan)
                else:
                    transferdata.append(w)
        transferdataDict[chiIndexList.pop(0)] = ''.join(transferdata)
        chiList.remove(contiChi)
        #chiIndexListCp = chiIndexListCp.pop(0)
        
    while nonchiList:
        noncontiChi = nonchiList[0]
        transferdata = []
        for w in noncontiChi:
            if w in specialmapping:
                transferdata.append(specialmapping[w])
            else:
                transfSymbol = strQ2B(w)
                transferdata.append(transfSymbol)
                if transfSymbol == w:
                    _transferSymbol_non.append(w)
        transferdataDict[nonchiIndexList.pop(0)] = ''.join(transferdata)
        nonchiList.remove(noncontiChi)
    transferdataDict = dict(sorted(transferdataDict.items(), key = lambda x:x[0]))
    _result = ''.join([item[1][1] for item in enumerate(transferdataDict.items())])
    while spaceIndex:
        index = spaceIndex.pop(0)
        _result = _result[:index]+' '+_result[index:]
    
    return _result,list(set(_transferSymbol_non))
    # for w in data:
    #     #print(w)
    #     if len(re.findall('([一-龥]+)',w)) > 0:
    #         index = hantoutf32(w)
    #         try:
    #             index16 = utf32toutf16(index)[3:-1].upper()
    #             #print(index16)
    #         except:
    #             print('check',w)
    #             continue
    #         if index16 in totalmapping:
    #             mappinghan = json.loads(utf32toutf16(totalmapping[index16]))
    #             transferdata.append(mappinghan)
    #         else:
    #             transferdata.append(w)
    #     else:
    #         if w in specialmapping:
    #             transferdata.append(specialmapping[w])
    #         else:
    #             transferdata.append(strQ2B(w))
    # return (''.join(transferdata))
def humansize(size):
    """将文件的大小转成带单位的形式
    >>> humansize(1024) == '1 KB'
    True
    >>> humansize(1000) == '1000 B'
    True
    >>> humansize(1024*1024) == '1 M'
    True
    >>> humansize(1024*1024*1024*2) == '2 G'
    True
    """
    units = ['B', 'KB', 'M', 'G', 'T']    
    for unit in units:
        if size < 1024:
            break
        size = size // 1024
    return '{} {}'.format(size, unit)
def humantime(seconds):
    """将秒数转成00:00:00的形式
    >>> humantime(3600) == '01:00:00'
    True
    >>> humantime(360) == '06:00'
    True
    >>> humantime(6) == '00:06'
    True
    """
    h = m = ''
    seconds = int(seconds)
    if seconds >= 3600:
        h = '{:02}:'.format(seconds // 3600)
        seconds = seconds % 3600
    if 1 or seconds >= 60:
        m = '{:02}:'.format(seconds // 60)
        seconds = seconds % 60
    return '{}{}{:02}'.format(h, m, seconds)
def processbar(pos, p2, fn, f_size, start):
    '''打印进度条
    just like:
    a.txt, 50.00% [=====     ] 1/2 [00:01<00:01]
    '''
    percent = min(pos * 10000 // p2, 10000)
    done = '=' * (percent//1000)
    half = '-' if percent // 100 % 10 > 5 else ''
    tobe = ' ' * (10 - percent//1000 - len(half))
    tip = '{}{}, '.format('\33[?25l', os.path.basename(fn))  #隐藏光标          
    past = time.time()-start
    remain = past/(percent+0.01)*(10000-percent)      
    print('\r{}{:.1f}% [{}{}{}] {:,}/{:,} [{}<{}]'.format(tip, 
            percent/100, done, half, tobe, 
            min(pos*int(f_size//p2+0.5), f_size), f_size, 
            humantime(past), humantime(remain)),
        end='')
    if percent == 10000:
        print('\33[?25h', end='')     # 显示光标
def wrap(wcounter,  fn, p1, p2, f_size):
    return wcounter.count_multi(fn, p1, p2, f_size)
    
class WordCN(object):
    def __init__(self, from_file, to_file=None, workers=None, coding=None,
                    max_direct_read_size=10000000):
        '''根據設定的進程數，把文件from_file分割等分，
        來讀取並統計詞頻，然後把結果寫入to_file中，當其為None時直接輸出。
        Args:
        @from_file 要讀取的文件
        @to_file 結果要寫入的文件
        @workers 進程數，為0時直接把文件一次性讀入內存；為1時按for line in open(xxx)
                讀取；>=2時為多進程分段讀取；默認為根據文件大小選擇0或cpu數量
        @coding 文件的編碼方式，默認為采用chardet模塊讀取前1萬個字符才自動判斷
        @max_direct_read_size 直接讀取的最大值，默認為10000000（約10M）
        
        How to use:
        w = WordCounter('a.txt', 'b.txt')
        w.run()        
        '''
        if not os.path.isfile(from_file):
            raise Exception('No such file: 文件不存在')
        self.f1 = from_file
        self.filesize = os.path.getsize(from_file)
        self.f2 = to_file
        if workers is None:
            if self.filesize < int(max_direct_read_size):
                self.workers = 0
            else:
                self.workers = cpu_count()# * 64 
        else:
            self.workers = int(workers)
        if coding is None:
            try:
                import chardet
            except ImportError:
                os.system('pip install chardet')
                print('-'*70)
                import chardet
            with open(from_file, 'rb') as f:    
                coding = chardet.detect(f.read(10000))['encoding']            
        self.coding = coding
        self._cnlist = []
        self.variants = []
        self._from_sets = []
        
        totalmapping = {}
        with open('hanMappingTable.txt','r',encoding='utf8') as f:
            totalmapping = json.loads(''.join(f.readlines()))
        self.totalmapping = totalmapping
        self.specialmapping = {'•':'§','╳':'§'}
        tradition = '廠幾兒虧與萬億個勺麼廣門義屍衛飛習馬鄉豐開無專扎藝廳區歷車岡貝見氣長僕幣僅從倉風勻烏鳳為憶訂計認隊辦勸書擊撲節術厲龍滅軋東業舊帥歸葉電號叨嘆們儀叢樂處鳥務飢閃蘭匯頭漢寧討寫讓禮訓議訊記遼邊發聖對糾絲動執鞏擴掃揚場亞朴機權過協壓厭頁奪達夾軌邁畢貞師塵當嚇蟲團嗎嶼歲豈剛則網遷喬偉傳優傷價華偽會殺眾爺傘創肌雜負壯沖莊慶劉齊產決閉問闖並關湯興講軍許論農諷設訪尋迅盡導異孫陣陽階陰婦媽戲觀歡買紅纖級約紀馳壽麥進遠違運撫壇壞擾壩貢搶墳坊護殼塊聲報蒼嚴蘆勞蘇極楊兩麗醫辰勵還殲來連堅時吳縣園曠圍噸郵員聽嗚崗帳財針釘亂體伶徹余鄰腸龜猶條飯飲凍狀畝況庫療應這棄冶閒間悶灶燦沃溝懷憂窮災證啟評補識訴診詞譯靈層遲張際陸陳勁雞驅純紗納綱駁縱紛紙紋紡驢紐環責現規攏揀擔頂擁勢攔撥擇蘋莖櫃槍構傑喪畫棗賣礦碼廁奮態歐壟轟頃轉斬輪軟齒虜腎賢國暢鳴詠羅幟嶺凱敗販購圖釣偵側憑僑貨質徑貪貧膚腫脹脅魚備飾飽飼變廟劑廢淨閘鬧鄭單爐淺淚瀉潑澤憐學寶審簾實試詩誠襯視話誕詢該詳肅錄隸屆陝限駕參艱線練組細駛織終駐駝紹經貫幫掛項撓趙擋墊擠揮薦帶繭蕩榮藥標棟欄樹咸磚砌牽殘輕鴉戰點臨覽豎削嘗顯啞貴蝦蟻螞雖罵嘩響峽罰賤鈔鐘鋼鑰鉤選適種復倆貸順儉須劍膽勝脈狹獅獨獄貿饒蝕餃餅彎將獎瘡瘋親聞閥閣養類逆總煉爛潔灑澆濁測濟渾濃惱舉覺憲竊語襖誤誘說誦墾晝險嬌賀壘綁絨結繞驕繪給絡駱絕絞統豔蠶頑撈載趕鹽損撿換熱恐壺蓮獲惡檔橋礎顧轎較頓斃慮監緊黨曬曉暈喚罷圓賊賄錢鉗鑽鐵鈴鉛犧敵積稱筆筍債傾艦艙愛頌胳髒膠腦皺餓戀槳漿離資閱煩燒燭遞濤澇潤漲燙湧寬賓請諸讀襪課誰調諒談誼剝懇劇難預絹驗繼掠職蘿營夢檢聾襲輔輛虛懸嶄銅鏟銀籠償銜盤鴿領臉獵餡館癢蓋斷獸漸漁滲慚驚慘慣窯謀謊禍謎彈隱嬸頸績緒續騎繩維綿綢綠趨擱摟攪聯確暫輩輝賞噴踐遺賭賠鑄鋪鏈銷鎖鋤鍋鏽鋒銳筐築篩儲懲釋臘魯饞蠻闊糞濕灣憤竄窩褲謝謠謙屬屢緞緩編騙緣攝擺攤鵲藍獻樓賴霧輸齡鑑錯錫鑼錘錦鍵鋸矮辭籌簽簡騰觸醬糧數滿濾濫滾濱灘譽謹縫纏牆願顆蠟蠅賺鍬鍛穩籮饅賽譜騾縮囑鎮顏額聰櫻飄瞞題顛贈鏡贊籃辯懶繳辮驟鐮侖譏鄧盧嘰爾馮迂籲吆倫鳧妝汛諱訝訛訟訣馱馴紉瑪韌摳掄塢擬蕪葦杈軒鹵嘔嗆嶇佃狽鳩廬閏兌瀝淪洶滄滬詛詐墜緯坯樞楓礬毆曇嚨賬貶貯俠僥劊覓龐瘧濘寵詭屜彌參紳駒絆繹貳挾莢蕎薺葷熒棧硯鷗軸勳喲鈣鈍鈉欽鈞鈕氫朧餌巒颯閨閩婁爍炫窪誡誣誨遜隕駭摯搗聶荸萊瑩鶯棲樺樁賈礫嘮鴦贓鉀鉚秫賃聳頒臍膿鴕鴛餒齋渦渙滌澗澀憫竅諾誹諄駿瑣麩擲撣摻螢蕭薩醞碩顱晤囉嘯邏銬鐺鋁鍘銑銘矯秸穢軀斂閻闡煥鴻淵諜諧襠袱禱謁謂諺頗綽繃綜綻綴瓊攬攙蔣韓頰靂翹鑿喳晾疇鵑賦贖賜銼鋅牘憊瘓滯潰濺謗緬纜締縷騷鵡欖輻輯頻蹺錨錐鍁錠錳頹膩鵬雛饃餾稟痺謄寢褂裸謬繽贅蔫藹鹼轅轄蟬鍍簫輿譚纓攆鑷鎬簍鯉癟癱瀾譴鶴繚轍鸚籬鯨瀕韁贍鐐鱷囂鰭癩攢鬢躪鑲'
        simple    = '厂几儿亏与万亿个勺么广门义尸卫飞习马乡丰开无专扎艺厅区历车冈贝见气长仆币仅从仓风匀乌凤为忆订计认队办劝书击扑节术厉龙灭轧东业旧帅归叶电号叨叹们仪丛乐处鸟务饥闪兰汇头汉宁讨写让礼训议讯记辽边发圣对纠丝动执巩扩扫扬场亚朴机权过协压厌页夺达夹轨迈毕贞师尘当吓虫团吗屿岁岂刚则网迁乔伟传优伤价华伪会杀众爷伞创肌杂负壮冲庄庆刘齐产决闭问闯并关汤兴讲军许论农讽设访寻迅尽导异孙阵阳阶阴妇妈戏观欢买红纤级约纪驰寿麦进远违运抚坛坏扰坝贡抢坟坊护壳块声报苍严芦劳苏极杨两丽医辰励还歼来连坚时吴县园旷围吨邮员听呜岗帐财针钉乱体伶彻余邻肠龟犹条饭饮冻状亩况库疗应这弃冶闲间闷灶灿沃沟怀忧穷灾证启评补识诉诊词译灵层迟张际陆陈劲鸡驱纯纱纳纲驳纵纷纸纹纺驴纽环责现规拢拣担顶拥势拦拨择苹茎柜枪构杰丧画枣卖矿码厕奋态欧垄轰顷转斩轮软齿虏肾贤国畅鸣咏罗帜岭凯败贩购图钓侦侧凭侨货质径贪贫肤肿胀胁鱼备饰饱饲变庙剂废净闸闹郑单炉浅泪泻泼泽怜学宝审帘实试诗诚衬视话诞询该详肃录隶届陕限驾参艰线练组细驶织终驻驼绍经贯帮挂项挠赵挡垫挤挥荐带茧荡荣药标栋栏树咸砖砌牵残轻鸦战点临览竖削尝显哑贵虾蚁蚂虽骂哗响峡罚贱钞钟钢钥钩选适种复俩贷顺俭须剑胆胜脉狭狮独狱贸饶蚀饺饼弯将奖疮疯亲闻阀阁养类逆总炼烂洁洒浇浊测济浑浓恼举觉宪窃语袄误诱说诵垦昼险娇贺垒绑绒结绕骄绘给络骆绝绞统艳蚕顽捞载赶盐损捡换热恐壶莲获恶档桥础顾轿较顿毙虑监紧党晒晓晕唤罢圆贼贿钱钳钻铁铃铅牺敌积称笔笋债倾舰舱爱颂胳脏胶脑皱饿恋桨浆离资阅烦烧烛递涛涝润涨烫涌宽宾请诸读袜课谁调谅谈谊剥恳剧难预绢验继掠职萝营梦检聋袭辅辆虚悬崭铜铲银笼偿衔盘鸽领脸猎馅馆痒盖断兽渐渔渗惭惊惨惯窑谋谎祸谜弹隐婶颈绩绪续骑绳维绵绸绿趋搁搂搅联确暂辈辉赏喷践遗赌赔铸铺链销锁锄锅锈锋锐筐筑筛储惩释腊鲁馋蛮阔粪湿湾愤窜窝裤谢谣谦属屡缎缓编骗缘摄摆摊鹊蓝献楼赖雾输龄鉴错锡锣锤锦键锯矮辞筹签简腾触酱粮数满滤滥滚滨滩誉谨缝缠墙愿颗蜡蝇赚锹锻稳箩馒赛谱骡缩嘱镇颜额聪樱飘瞒题颠赠镜赞篮辩懒缴辫骤镰仑讥邓卢叽尔冯迂吁吆伦凫妆汛讳讶讹讼诀驮驯纫玛韧抠抡坞拟芜苇杈轩卤呕呛岖佃狈鸠庐闰兑沥沦汹沧沪诅诈坠纬坯枢枫矾殴昙咙账贬贮侠侥刽觅庞疟泞宠诡屉弥叁绅驹绊绎贰挟荚荞荠荤荧栈砚鸥轴勋哟钙钝钠钦钧钮氢胧饵峦飒闺闽娄烁炫洼诫诬诲逊陨骇挚捣聂荸莱莹莺栖桦桩贾砾唠鸯赃钾铆秫赁耸颁脐脓鸵鸳馁斋涡涣涤涧涩悯窍诺诽谆骏琐麸掷掸掺萤萧萨酝硕颅晤啰啸逻铐铛铝铡铣铭矫秸秽躯敛阎阐焕鸿渊谍谐裆袱祷谒谓谚颇绰绷综绽缀琼揽搀蒋韩颊雳翘凿喳晾畴鹃赋赎赐锉锌牍惫痪滞溃溅谤缅缆缔缕骚鹉榄辐辑频跷锚锥锨锭锰颓腻鹏雏馍馏禀痹誊寝褂裸谬缤赘蔫蔼碱辕辖蝉镀箫舆谭缨撵镊镐篓鲤瘪瘫澜谴鹤缭辙鹦篱鲸濒缰赡镣鳄嚣鳍癞攒鬓躏镶'
        self.s2t = {}
        for index in range(len(tradition)):
            self.s2t[simple[index]] = tradition[index]
        self._STtransfer = []
        self._transferSymbol_non = []
    def Normalize(self,data):
        spaceIndex = [m.start() for m in re.finditer('(\s)',data)]
        data = data.replace(' ','')
        chiIndexList = [m.start() for m in re.finditer('([一-龥]+)',str(data))]
        chiList = re.findall('([一-龥]+)',str(data))
        nonchiIndexList = [m.start() for m in re.finditer('([^一-龥]+)',str(data))]
        nonchiList = [item for item in re.sub('([一-龥]+)',' ',str(data)).split(' ') if not item == '']
        transferdataDict = {}
        while chiList:
            contiChi = chiList[0]
            transferdata = []
            for w in contiChi:
                if w in self.s2t:
                    self._STtransfer.append(w)
                    transferdata.append(self.s2t[w])
                else:
                    index = hantoutf32(w)
                    try:
                        index16 = utf32toutf16(index)[3:-1].upper()
                    except:
                        print('check',w)
                        continue
                    if index16 in self.totalmapping:
                        self.variants.append(w)
                        mappinghan = json.loads(utf32toutf16(self.totalmapping[index16]))
                        #print(index16,w,mappinghan)
                        transferdata.append(mappinghan)
                    else:
                        transferdata.append(w)
            transferdataDict[chiIndexList.pop(0)] = ''.join(transferdata)
            chiList.remove(contiChi)
        while nonchiList:
            noncontiChi = nonchiList[0]
            transferdata = []
            for w in noncontiChi:
                if w in self.specialmapping:
                    transferdata.append(self.specialmapping[w])
                else:
                    transfSymbol = strQ2B(w)
                    transferdata.append(transfSymbol)
                    if transfSymbol == w:
                        self._transferSymbol_non.append(w)
            transferdataDict[nonchiIndexList.pop(0)] = ''.join(transferdata)
            nonchiList.remove(noncontiChi)
        transferdataDict = dict(sorted(transferdataDict.items(), key = lambda x:x[0]))
        _result = ''.join([item[1][1] for item in enumerate(transferdataDict.items())])
        while spaceIndex:
            index = spaceIndex.pop(0)
            _result = _result[:index]+' '+_result[index:]
        #print(set(self.variants))
        return _result
        # transferdata = []
        # for w in data:
        #     #print(w)
        #     if len(re.findall('([一-龥]+)',w)) > 0:
        #         index = hantoutf32(w)
        #         try:
        #             index16 = utf32toutf16(index)[3:-1].upper()
        #             #print(index16)
        #         except:
        #             print('check',w)
        #             continue
        #         if index16 in self.totalmapping:
        #             mappinghan = json.loads(utf32toutf16(self.totalmapping[index16]))
        #             transferdata.append(mappinghan)
        #         else:
        #             transferdata.append(w)
        #     else:
        #         if w in self.specialmapping:
        #             transferdata.append(self.specialmapping[w])
        #         else:
        #             transferdata.append(strQ2B(w))
        # return (''.join(transferdata))

    def run(self):
        start = time.time()
        if self.workers == 0:
            self.count_direct(self.f1)
        elif self.workers == 1:
            self.count_single(self.f1, self.filesize)
        else:
            try:
                pool = Pool(self.workers)
                res_list = []
                for i in range(self.workers):
                    #print('start process:',i)
                    p1 = self.filesize * i // self.workers 
                    p2 = self.filesize * (i+1) // self.workers 
                    args = [self, self.f1, p1, p2, self.filesize]
                    res = pool.apply_async(func=wrap, args=args)
                    res_list.append(res)
                    #res_list.append(res.get())
                    #print('\n',i,res.get())
                pool.close()
                pool.join()
                for r in res_list:
                    datacouple = r.get()
                    self._cnlist.extend(datacouple[0])
                    self.variants.extend(datacouple[1])
                    self._transferSymbol_non.extend(datacouple[2])
                

                #[self._cnlist.extend(r.get()) for r in res_list]
                
            except KeyboardInterrupt:
                #pool.terminate()
                pool.close()
                pool.join()
                print('nonononononon')
            
                            
        if self.f2:
            print('\nwriting now')
            with open(self.f2, 'wb') as f:
                f.write(self.result.encode(self.coding))
                #f.write(b'\n')
        else:
            print(self.result)
        cost = '{:.1f}'.format(time.time()-start)
        size = humansize(self.filesize)
        tip = 'File size: {}. Workers: {}. Cost time: {} seconds'     
        print(tip.format(size, self.workers, cost))
        self.cost = cost + 's'
        #transfer character
        print(set(self.variants))
        # not transfer symbol
        print(set(self._transferSymbol_non))
                
    def count_single(self, from_file, f_size):
        '''单进程读取文件并统计词频'''
        start = time.time()
        with open(from_file, 'rb') as f:
            for line in f:
                self._cnlist.append(self.parse(line))
                processbar(f.tell(), f_size, from_file, f_size, start)   

    def count_direct(self, from_file):
        '''直接把文件内容全部读进内存并统计词频'''
        print('countdirect')
        start = time.time()
        with open(from_file, 'rb') as f:
            for line in f:
                self._cnlist.append(self.parse(line))  
            #line = f.read()
        
                
    def count_multi(self, fn, p1, p2, f_size):  
        #print(p1,p2,f_size)
        cnlist = []
        with open(fn, 'rb') as f:    
            if p1:  # 为防止字被截断的，分段处所在行不处理，从下一行开始正式处理
                f.seek(p1-1)
                while b'\n' not in f.read(1):
                    if f.tell() >= p2:
                        return []
            start = time.time()
            try:
                while 1:                           
                    line = f.readline()
                    if not line == b'':
                        cnlist.append((self.parse(line)))
                        #print(cnlist)
                    pos = f.tell()  
                    if p1 == 0: #显示进度
                        processbar(pos, p2, fn, f_size, start)
                    if pos >= p2:         
                        return cnlist,self.variants,self._transferSymbol_non
            except KeyboardInterrupt:
                #print(cnlist)
                #print('here')
                return cnlist 
                #return 
    def parse(self, line):  #解析读取的文件流
        #return re.sub(r'\s+','',line.decode(self.coding))
        return self.Normalize(re.sub(r'\s+','',line.decode(self.coding)))
        
    def flush(self):  #清空统计结果
        self._cnlist = []

    @property
    def counter(self):  #返回统计结果的Counter类       
        return self._cnlist
    
    @property
    def result(self):  #返回统计结果的字符串型式，等同于要写入结果文件的内容
        #ss = ['{}: {}'.format(i, j) for i, j in self._c.most_common()]
        result = '\n'.join(self._cnlist)
        #print(result) 
        return result

def main():
    #load parameter:
    #file in file out or str in str out
    import argparse
    import os.path
    import multiprocessing  as mp
    parser = argparse.ArgumentParser("Script for graphmome")
    parser.add_argument("-S","--strONOFF", type=str, required=True,help='define input output method')
    parser.add_argument("-s","--strin", type=str ,help='define input output method')
    parser.add_argument("-fin","--filename", type=str ,help='input filename')
    parser.add_argument("-fout","--tofile", type=str ,help='ouput filename')
    args = parser.parse_args()
    
    if args.strONOFF == 'True':
        # python3 .\main.py --strONOFF=True --strin='測#＃試，•'
        try:
            data = args.strin
            normalizeResult = strNormalize(data)
            print(normalizeResult[0]+'\n'+' '.join(normalizeResult[1]))
        except Exception as e:
            print('your should give me some string',e)
    else:
        #check file size
        # if len(sys.argv) < 2:
        #     print('Usage: python wordcounter.py from_file to_file')
        #     exit(1)
        #from_file, to_file = sys.argv[1:3]
        from_file = args.filename
        try:
            to_file = args.tofile
        except:
            to_file = None
        args = {'coding' : 'utf8', 'workers':None, 'max_direct_read_size':10000000}
        for i in sys.argv:
            for k in args:
                if re.search(r'{}=(.+)'.format(k), i):
                    args[k] = re.findall(r'{}=(.+)'.format(k), i)[0]
        w = WordCN(from_file, to_file, **args)
        w.run() 
        

if __name__ == '__main__':
    main()



