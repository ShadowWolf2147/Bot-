import discord  
from discord.ext import commands  
import os
import random
import requests


intents = discord.Intents.default()  
intents.message_content = True 
intents.members = True


bot = commands.Bot(command_prefix='$', intents=intents)



@bot.event  
async def on_ready(): 
    print(f'{bot.user} olarak giriş yaptık')  


@bot.command()  
async def hello(ctx):  
    await ctx.send(f'Merhaba {bot.user}! Ben bir botum!')




@bot.command()  
async def joined(ctx, member: discord.Member):  
    """Bir kişinin sunucuya ne zaman katıldığını söyler."""

    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = f'Welcome {member.mention} to {guild.name}!'
            await guild.system_channel.send(to_send)

@bot.command()
async def mem(ctx):
    try:
        
        files = os.listdir('images')
        if not files:  
            await ctx.send("Resim klasörü boş!")
            return
        
    
        img_name = random.choice(files)
        
    
        with open(f'images/{img_name}', 'rb') as f:
            picture = discord.File(f)
        await ctx.send(file=picture)
    except FileNotFoundError:
        await ctx.send("Resim klasörü bulunamadı! Lütfen 'images' klasörünün mevcut olduğundan emin olun.")
    except Exception as e:
        await ctx.send(f"Bir hata oluştu: {e}")

def get_duck_image_url():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']


@bot.command('duck')
async def duck(ctx):
    '''duck komutunu çağırdığımızda, program ordek_resmi_urlsi_al fonksiyonunu çağırır.'''
    image_url = get_duck_image_url()
    await ctx.send(image_url)

cevre = [
    "Tek kullanımlık plastik yerine tekrar kullanılabilir ürünler tercih edin.",
    "Enerji tasarrufu için kullanılmayan cihazları prizden çekin.",
    "Yerel çiftçilerden alışveriş yaparak karbon ayak izinizi azaltın.",
    "Toplu taşıma kullanın veya bisiklete binerek fosil yakıt tüketimini azaltın.",
    "Kağıt israfını önlemek için dijital notlar alın.",
    "Geri dönüştürülebilir atıkları doğru şekilde ayırın.",
    "Yanınızda bir su şişesi taşıyarak plastik şişe kullanımını azaltın.",
    "Bahçenizde kompost yaparak organik atıkları değerlendirin.",
    "Doğal temizlik malzemeleri kullanarak kimyasal kirliliği azaltın.",
    "Ağaç dikerek çevrenize katkıda bulunun."
]

@bot.command()
async def cevredostu(ctx):
    tip = random.choice(cevre)
    await ctx.send(f"\ud83c\udf3f {tip}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "merhaba" in message.content.lower():
        await message.channel.send("Merhaba! \ud83d\ude04 Çevre dostu fikirler için `$cevredostu` komutunu kullanabilirsiniz.")

    await bot.process_commands(message)

bot.run("TOKEN")
