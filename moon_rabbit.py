import discord
from discord.ext import commands
import requests
import json
import random
from selenium import webdriver
import server_name_converter
import time
import os
from boto.s3.connection import S3Connection


app = commands.Bot(command_prefix="#")

discord_api_key = S3Connection(os.environ['discord_api_key'])
neople_api_key = S3Connection(os.environ['neople_api_key'])
browser_options = webdriver.ChromeOptions()
browser_options.add_argument('headless')
browser_options.add_argument('window-size=1920x1080')
browser_options.add_argument("disable-gpu")
browser = webdriver.Chrome('chromedriver', options=browser_options)


@app.event
async def on_ready():
    print("다음으로 로그인합니다: ", end="")
    print(app.user.name)
    print("Connection was successful. ")
    await app.change_presence(status=discord.Status.online, activity=discord.Game("던전앤파이터"))


@app.command(name='명령어')
async def help_command(ctx):
    embed = discord.Embed(title='명령어를 알려줄게!', color=discord.Color.blue())
    embed.set_thumbnail(url='https://www.city.kr/files/attach/images/161/715/991/005/169199853332e0e576fd914f085c0b5a.gif')
    embed.add_field(name='#딜', value='1시딜을 알려줍니다.\nex) #딜 $P 또는 #딜 카인 $P\n서버명을 입력하지 않으면 카인 서버로 검색', inline=False)
    embed.add_field(name='#버프력', value='버프력을 알려줍니다.\nex) #버프력 오야븜미 또는 #버프력 카인 오야븜미\n서버명을 입력하지 않으면 카인 서버로 검색', inline=False)
    embed.add_field(name='#닉', value='사용 가능한 닉네임의 서버를 알려줍니다..\nex) #닉 $P', inline=False)
    embed.add_field(name='#머먹지', value='메뉴를 추천해줍니다.', inline=False)
    embed.add_field(name='#닉넴수', value='던파 서버에서 사용중인 닉네임 수를 알려줍니다.', inline=False)
    await ctx.send(embed=embed)


@app.command(name='핑')
async def ping(ctx, number: int):
    await ctx.send(number)


@app.command(name='잘자')
async def ping(ctx):
    await ctx.send('https://blogimg.goo.ne.jp/user_image/44/3a/b2ec2e835264fc5abae347e8721f1748.gif')


@app.command(name='화이팅')
async def ping(ctx):
    await ctx.send('https://media.tenor.com/images/da43d28ce922ccf6c36359c11ead912d/tenor.gif')


@app.command(name='박수')
async def ping(ctx):
    await ctx.send('와! 짝짝짝!!')


@app.command(name="머먹지")
async def random_menu(ctx):
    lst = ["피자", "치킨", "마라탕", "찜닭", "라면", "굶어", "햄버거", "홍어", "토끼구이", "떡볶이", "족발", "중국집", "빵과 우유", "돈까스", "불고기"]
    await ctx.send(lst[random.randrange(0, len(lst))]+" ㅇㅅㅇ")


@app.command(name='스샷')
async def get_character_image(ctx, *input: str):
    if len(input) is 1:
        char_name = str(input[0])
        URL = "https://api.neople.co.kr/df/servers/cain/characters?characterName="
        URL += char_name
        URL += neople_api_key
        response = requests.get(URL).text
        new_response = response.replace("'", "\"")
        dict_data = (json.loads(new_response)).get('rows')[0]
        char_id = dict_data.get('characterId')
        picture = 'https://img-api.neople.co.kr/df/servers/cain/characters/'+char_id+'?zoom=2'
        embed = discord.Embed(title=dict_data.get('characterName'), color=discord.Color.blue())
        embed.set_image(url=picture)

        await ctx.send(embed=embed)

    else:
        server_kor = str(input[0])
        char_name = str(input[1])
        server_eng = server_name_converter.to_eng(server_kor)

        URL = "https://api.neople.co.kr/df/servers/"
        URL += server_eng
        URL += "/characters?characterName="
        URL += char_name
        URL += neople_api_key
        response = requests.get(URL).text
        new_response = response.replace("'", "\"")
        dict_data = (json.loads(new_response)).get('rows')[0]
        char_id = dict_data.get('characterId')
        picture = 'https://img-api.neople.co.kr/df/servers/'+server_eng+'/characters/'+char_id+'?zoom=2'
        embed = discord.Embed(title=dict_data.get('characterName'), color=discord.Color.blue())
        embed.set_image(url=picture)

        await ctx.send(embed=embed)


@app.command(name='닉넴수')
async def how_many_nicknames(ctx, input: str):
    URL = "https://api.neople.co.kr/df/servers/all/characters?characterName="
    URL += input
    URL += neople_api_key
    response = requests.get(URL).text
    new_response = response.replace("'", "\"")
    dict_data = json.loads(new_response)
    await ctx.send("["+input+"] 의 닉네임 개수는 "+str(len(dict_data.get('rows')))+"개에요 ㅇㅅㅇ")


@app.command(name='닉')
async def how_many_nicknames(ctx, input: str):
    URL = "https://api.neople.co.kr/df/servers/all/characters?characterName="
    URL += input
    URL += neople_api_key
    response = requests.get(URL).text
    new_response = response.replace("'", "\"")
    dict_data = (json.loads(new_response)).get('rows')
    server_list = ['cain', 'diregie', 'siroco', 'prey', 'casillas', 'hilder', 'anton', 'bakal']
    for data in dict_data:
        server_list.remove(data.get('serverId'))
    # 사용가능 서버명을 한글로 바꾸기
    server_list_kor = []
    for a in server_list:
        if 'cain' in a:
            server_list_kor.append("카인")
        if 'diregie' in a:
            server_list_kor.append("디레지에")
        if 'siroco' in a:
            server_list_kor.append("시로코")
        if 'prey' in a:
            server_list_kor.append("프레이")
        if 'casillas' in a:
            server_list_kor.append("카시야스")
        if 'hilder' in a:
            server_list_kor.append("힐더")
        if 'anton' in a:
            server_list_kor.append("안톤")
        if 'bakal' in a:
            server_list_kor.append("바칼")
    if len(server_list_kor) == 0:
        await ctx.send("닉네임 ["+input+"]은 사용이 불가능해요... ㅇㅅㅇ")
    else:
        await ctx.send("닉네임 ["+input+"]을 쓸 수 있는 서버에요 ㅇㅅㅇ\n"+str(server_list_kor))


@app.command(name='딜')
async def get_deal(ctx, *input: str):
    if len(input) is 1:
        char_name = str(input[0])
        URL = "https://api.neople.co.kr/df/servers/cain/characters?characterName="
        URL += char_name
        URL += neople_api_key
        response = requests.get(URL).text
        new_response = response.replace("'", "\"")
        dict_data = (json.loads(new_response)).get('rows')[0]
        char_id = dict_data.get('characterId')

        DUNOFF = "https://dunfaoff.com/SearchResult.df?server=cain&characterid="
        DUNOFF += char_id

        print("던오프 요청 ->"+DUNOFF)

        browser.get(DUNOFF)
        browser.implicitly_wait(1)
        browser.find_element_by_xpath('//*[@id="damage_side"]').click()
        browser.implicitly_wait(1)
        browser.find_element_by_xpath('//*[@id="skill_damage"]/ul/li[4]').click()
        browser.implicitly_wait(1)
        browser.find_element_by_xpath('//*[@id="skill_damage"]/div[2]/div[2]/div/label[3]').click()
        browser.implicitly_wait(2)
        output = browser.find_element_by_class_name('sinergeDmg1').text
        browser.get(DUNOFF)

        _output_num = int(output.replace(',', ''))
        if _output_num >= 100000000:
            await ctx.send("[카인 - "+char_name+"]님의 딜은 ["+str(int(_output_num/100000000))+"억] 이에요!!! ㅇㅅㅇ")
        else:
            await ctx.send("[카인 - "+char_name+"]님의 딜은 ["+output+"] 에요!!! ㅇㅅㅇ")
    else:
        server_kor = str(input[0])
        char_name = str(input[1])
        server_eng = server_name_converter.to_eng(server_kor)

        URL = "https://api.neople.co.kr/df/servers/"
        URL += server_eng
        URL += "/characters?characterName="
        URL += char_name
        URL += neople_api_key
        response = requests.get(URL).text
        new_response = response.replace("'", "\"")
        dict_data = (json.loads(new_response)).get('rows')[0]
        char_id = dict_data.get('characterId')

        DUNOFF = "https://dunfaoff.com/SearchResult.df?server="
        DUNOFF += server_eng
        DUNOFF += "&characterid="
        DUNOFF += char_id

        print("던오프 요청 ->"+DUNOFF)

        browser.get(DUNOFF)
        browser.implicitly_wait(1)
        browser.find_element_by_xpath('//*[@id="damage_side"]').click()
        browser.implicitly_wait(1)
        browser.find_element_by_xpath('//*[@id="skill_damage"]/ul/li[4]').click()
        browser.implicitly_wait(1)
        browser.find_element_by_xpath('//*[@id="skill_damage"]/div[2]/div[2]/div/label[3]').click()
        browser.implicitly_wait(2)
        output = browser.find_element_by_class_name('sinergeDmg1').text
        browser.get(DUNOFF)

        _output_num = int(output.replace(',', ''))
        if _output_num >= 100000000:
            await ctx.send("[카인 - "+char_name+"]님의 딜은 ["+str(int(_output_num/100000000))+"억] 이에요!!! ㅇㅅㅇ")
        else:
            await ctx.send("[" + server_kor + " - " + char_name + "]님의 딜은 [" + output + "] 에요!!! ㅇㅅㅇ")


@app.command(name='버프력')
async def get_deal(ctx, *input: str):
    if len(input) is 1:
        char_name = str(input[0])
        URL = "https://api.neople.co.kr/df/servers/cain/characters?characterName="
        URL += char_name
        URL += neople_api_key
        response = requests.get(URL).text
        new_response = response.replace("'", "\"")
        dict_data = (json.loads(new_response)).get('rows')[0]
        char_id = dict_data.get('characterId')

        DUNOFF = "https://dunfaoff.com/SearchResult.df?server=cain&characterid="
        DUNOFF += char_id

        print("던오프 요청 ->"+DUNOFF)

        browser.get(DUNOFF)
        browser.implicitly_wait(1)
        browser.find_element_by_xpath('//*[@id="holy_buff_side"]').click()
        browser.implicitly_wait(1)
        output = browser.find_element_by_xpath('//*[@id="holy_buff_list"]/div[1]/div[2]/div[10]/div/a').text
        browser.get(DUNOFF)
        await ctx.send("[카인 - "+char_name+"]님의 버프력은 ["+output+"] 에요!!! ㅇㅅㅇ")
    else:
        server_kor = str(input[0])
        char_name = str(input[1])
        server_eng = server_name_converter.to_eng(server_kor)

        URL = "https://api.neople.co.kr/df/servers/"
        URL += server_eng
        URL += "/characters?characterName="
        URL += char_name
        URL += neople_api_key
        response = requests.get(URL).text
        new_response = response.replace("'", "\"")
        dict_data = (json.loads(new_response)).get('rows')[0]
        char_id = dict_data.get('characterId')

        DUNOFF = "https://dunfaoff.com/SearchResult.df?server="
        DUNOFF += server_eng
        DUNOFF += "&characterid="
        DUNOFF += char_id

        print("던오프 요청 ->"+DUNOFF)

        browser.get(DUNOFF)
        browser.implicitly_wait(1)
        browser.find_element_by_xpath('//*[@id="holy_buff_side"]').click()
        browser.implicitly_wait(1)
        output = browser.find_element_by_xpath('//*[@id="holy_buff_list"]/div[1]/div[2]/div[10]/div/a').text
        browser.get(DUNOFF)
        await ctx.send("["+server_kor+" - " + char_name + "]님의 버프력은 [" + output + "] 에요!!! ㅇㅅㅇ")


@app.command(name="시세")
async def find_items_in_auction(ctx, *input: str):
    URL = "https://api.neople.co.kr/df/auction?itemName="
    for a in input:
        URL += "+"+str(a)
    URL +="&limit=3&sort=unitPrice:asc&wordType=full"
    URL += neople_api_key
    print("URL ->"+URL)
    response = requests.get(URL).text
    new_response = response.replace("'", "\"")
    arr_data = (json.loads(new_response)).get('rows')
    if arr_data is None:
        await ctx.send("검색어를 다르게 한번... 해보심이... ㅇㅅㅇ")
    else:
        embed = discord.Embed(title='아이템 검색 결과 (베타)', color=discord.Color.blue())
        embed.set_thumbnail(url=("https://img-api.neople.co.kr/df/items/"+arr_data[0].get('itemId')))
        for data in arr_data:
            embed.add_field(name=data.get('itemName'), value='가격: '+str(data.get('unitPrice'))+'골드, 개수'+str(data.get('count'))+'개', inline=False)
        await ctx.send(embed=embed)


@app.command(name="오늘")
async def what_day_today(ctx):
    t = ["월요일 : 헬이나 도세요", "화요일 : 헬이나 도세요", "수요일 : 홍옥의 저주", "목요일 : 오큘러스, 산맥, 마대, 조안 페레로 3종던전", "금요일 : 오큘러스, 산맥, 마대", "토요일 : 레이드", "일요일 : 레이드"]
    n = time.localtime().tm_wday
    await ctx.send("오늘은 "+t[n])


app.run(discord_api_key)
