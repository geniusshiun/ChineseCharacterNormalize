

def main():
    from CNtool import hantoutf32,utf32toutf16,rangereturn,loaddict
    import json
    import re

    unicodeToVar,unicodeToFrequency,unicodeTokGradeLevel,unicodeTokHanyuPinyin,unicodeTokMandarin = loaddict()
    start = ['0x3400', '0x4E00', '0xF900', '0x20000', '0x2A700','0x2B740','0x2B820']
    end = ['0x4DBF', '0x9FD5' , '0xFAFF', '0x2A6DF', '0x2B73F', '0x2B81F', '0x2CEA1']
    totalcnt = 0
    if len(start) != len(end):
        print('some error')
    KZ_Semantic_vardict = []
    SpecialSemanticvardict = []

    for codeindex in range(len(start)):
        init = int(start[codeindex],16)
        thisturnVariant = []
        while init <= int(end[codeindex],16):
            totalcnt+=1
            code = hex(init)[2:]
            unicode16 = utf32toutf16(hex(init))
            
            hanzi = json.loads(unicode16)
            index = code.upper()
            #find index(self)'s propety
            if index in unicodeToVar:
                frequency = 'no Frequency'
                kGradeLevel = 'no GradeLevel'
                if index in unicodeToFrequency:
                    #print(unicodeToFrequency[index]['value'],end = ' ')
                    frequency = unicodeToFrequency[index]['value']
                if index in unicodeTokGradeLevel:
                    kGradeLevel = unicodeTokGradeLevel[index]['value']
                indexproperty = {}
                indexproperty['Frequency'] = frequency
                indexproperty['GradeLevel'] = kGradeLevel
                #print(hanzi,index,indexproperty)
                vardict = {}
                specialvardict = {}
                variants = []
                specialcode = []
                simplehan = []
                Semantic = []
                
                
                #find other variant propety
                for var in unicodeToVar[index]:
                    #Maybe, there are more than one mapping in unicodeToVar[index]
                    if var['type'] == 'kSpecializedSemanticVariant':
                        for uni in re.findall(r'\+([A-Z0-9]+)',var['mapping']):
                            if len(uni) >= 4:
                                if not uni in specialcode:
                                    specialcode.append(uni)
                    elif var['type'] == 'kTraditionalVariant':
                        for uni in re.findall(r'\+([A-Z0-9]+)',var['mapping']):
                            if len(uni) >= 4:
                                if not uni in simplehan:
                                    simplehan.append(uni)
                    elif var['type'] == 'kSemanticVariant':
                        for uni in re.findall(r'\+([A-Z0-9]+)',var['mapping']):
                            if len(uni) >= 4:
                                if not uni in Semantic:
                                    Semantic.append(uni)
                    else:
                        #print(index,var)
                        if var['type'] == 'kSimplifiedVariant':
                            continue
                        for uni in re.findall(r'\+([A-Z0-9]+)',var['mapping']):
                            if len(uni) >= 4:
                                if not uni in variants:
                                    variants.append(uni)
                
                for uni in specialcode: 
                    tmpdict = {}
                    if not uni in tmpdict:
                        if uni in unicodeToFrequency:
                            #specialvardict[uni] = unicodeToFrequency[uni]['value']
                            tmpdict['Frequency']= unicodeToFrequency[uni]['value']
                        else:
                            tmpdict['Frequency'] = 'no Frequency'
                            
                        if uni in unicodeTokGradeLevel:
                            tmpdict['GradeLevel'] = unicodeTokGradeLevel[uni]['value']
                        else:
                            tmpdict['GradeLevel'] = 'no GradeLevel'
                        specialvardict[uni] = tmpdict
                if specialvardict:
                    specialvardict[index] = indexproperty
                    SpecialSemanticvardict.append(specialvardict)
                
                for uni in variants: 
                    tmppropety = {}
                    if not uni in tmppropety:
                        if uni in unicodeToFrequency:
                            tmppropety['Frequency'] = unicodeToFrequency[uni]['value']
                            #vardict[uni] = unicodeToFrequency[uni]['value']
                        else:
                            tmppropety['Frequency'] = 'no Frequency'
                            #vardict[uni] = 'no Frequency'
                        if uni in unicodeTokGradeLevel:
                            tmppropety['GradeLevel'] = unicodeTokGradeLevel[uni]['value']
                        else:
                            tmppropety['GradeLevel'] = 'no GradeLevel'
                        vardict[uni] = tmppropety
                if vardict:
                    vardict[index] = indexproperty
                    bigdict = {}
                    bigdict[index] = vardict
                    KZ_Semantic_vardict.append(bigdict)      
                    thisturnVariant.append(bigdict)
            init+=1
        #print(len(thisturnVariant),unicode16)
        #print('='*10)
    cnt_not_sure = 0
    find_one = 0
    totalmapping = {}
    for group in KZ_Semantic_vardict:
        #print(group)
        inrange = []
        for index,workgroup in group.items():
            frequencyexists = []
            GradeLevelexists = []
            inrange = []
            TraditionalSets = []
            lensequalfours = []
            #find Minimal frequency
            for key, val in workgroup.items():
                if workgroup[key]['Frequency'] != 'no Frequency':
                    if not frequencyexists:
                        frequencyexists.append(key)
                    #replace Minimal frequency
                    else:
                        if int(workgroup[key]['Frequency']) < int(workgroup[frequencyexists[0]]['Frequency']):
                            frequencyexists = []
                            frequencyexists.append(key)
                        elif int(workgroup[key]['Frequency']) == int(workgroup[frequencyexists[0]]['Frequency']):
                            frequencyexists.append(key)
                if workgroup[key]['GradeLevel'] != 'no GradeLevel':
                    if not GradeLevelexists:
                        GradeLevelexists.append(key)
                    #replace Minimal frequency
                    else:
                        if int(workgroup[key]['GradeLevel']) < int(workgroup[GradeLevelexists[0]]['GradeLevel']):
                            GradeLevelexists = []
                            GradeLevelexists.append(key)
                        elif int(workgroup[key]['GradeLevel']) == int(workgroup[GradeLevelexists[0]]['GradeLevel']):
                            GradeLevelexists.append(key)
                if int(key,16)>int('4E00',16) and int(key,16)<int('9FA5',16):
                    inrange.append(key)
                if len(key) <= 4:
                    lensequalfours.append(key)
            #print(index,frequencyexists,GradeLevelexists)
            for item in unicodeToVar[index]:
                if item['type'] == 'kTraditionalVariant':
                    TraditionalSets.append(item['mapping'][2:])
            
            #make dicision
            if len(frequencyexists) == 1:
                totalmapping[index] = frequencyexists[0]
            elif len(GradeLevelexists) == 1:
                totalmapping[index] = GradeLevelexists[0]
            elif len(inrange) == 1:
                totalmapping[index] = inrange[0]
            #elif len(TraditionalSets) == 1:
            #    totalmapping[index] = TraditionalSets[0]
            elif len(lensequalfours) == 1:
                totalmapping[index] = lensequalfours[0]
            else:
                unicode16 = utf32toutf16(key)
                hanzi = json.loads(unicode16)
                #print(hanzi,workgroup)
            
                #find one
            #if index in totalmapping:
            #    print(totalmapping[index],frequencyexists,GradeLevelexists,inrange,TraditionalSets)
            #else:
            #    print('find one',frequencyexists,GradeLevelexists,inrange,TraditionalSets)
            """
            if not frequencyexists and not GradeLevelexists and not inrange and not TraditionalSets and not fours:
                cnt_not_sure+=1
            else:
                find_one+=1
            print('check',cnt_not_sure)        
            print('find',find_one)        
            """
    newtotalmapping = totalmapping.copy()
    try:
        with open('removeMapping.txt','r',encoding='utf8') as f:
            removelist = [n.strip() for n in f.readlines()]
    except:
        removelist = []
    try:
        with open('reading_skip.txt','r',encoding='utf8') as f:
            readingskip = [n.strip() for n in f.readlines()]
    except:
        readingskip = []
    for key,val in totalmapping.items():
        hanzi = json.loads(utf32toutf16(key))
        if hanzi in readingskip:
            continue
        if (key in unicodeTokHanyuPinyin) and (val in unicodeTokHanyuPinyin):
            retSets = [i for i in unicodeTokHanyuPinyin[key]['value'] if i in unicodeTokHanyuPinyin[val]['value']]
            if len(retSets) == 0:
                #alought in HanyuPinyin but have no Intersection    
                print(hanzi,unicodeTokHanyuPinyin[key]['value'],json.loads(utf32toutf16(val)),unicodeTokHanyuPinyin[val]['value'])        
                del newtotalmapping[key]
        else:
            #not in HanyuPinyin but maybe have the same Mandarin
            if (key in unicodeTokMandarin) and (val in unicodeTokMandarin):
                if unicodeTokMandarin[key]['value'] != unicodeTokMandarin[val]['value']:
                    print(hanzi,unicodeTokMandarin[key]['value'],json.loads(utf32toutf16(val)),unicodeTokMandarin[val]['value'])
                    del newtotalmapping[key]
            #else:
            #    print(json.loads(utf32toutf16(key)),json.loads(utf32toutf16(val)),'all not in')
            #    del newtotalmapping[key]
        
        if hanzi in removelist:
            print(hanzi,'remove')
            del newtotalmapping[key]
        
    print(len(newtotalmapping))
    with open('hanMappingTable.txt','w',encoding='utf8') as f:
        f.write(json.dumps(newtotalmapping))
    #print(json.loads(utf32toutf16(totalmapping[hantoutf32('里')])))
    #print(totalmapping['91CC'])
if __name__ == '__main__':
    main()