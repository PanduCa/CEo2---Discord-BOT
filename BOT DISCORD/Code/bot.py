#//////////////////////////////IMPORTS///////////////////////////////////////////////
import discord
from discord.ext import commands
import time
import os
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

#/////////////////////////INTENTS//////////////////////////////////////////////
description = '''c!help'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.messages = True

#///////////////////////////////////VAR////////////////////////////////////////////#
prefix = "c!"

#////////////////////////////////////////////BOT///////////////////////////////////
bot = commands.Bot(command_prefix=prefix, description=description, intents=intents)
load_dotenv()
bot_token = os.getenv("TOKEN") 
if not bot_token:
    raise ValueError("TOKEN no se encuentra en el archivo .env.")

#//////////////////////////////////////////DATABASE/////////////////////////////////////
user_bd = {}
transporte_bd = {}
transporte_bd_r = []        
tipo_transporte_bd = {}
recurrencia_bd = {}
distancia_bd = {}
por_semana_bd = {}
por_mes_bd = {}
vuelos_bd = {}
luces_bd = {}

pregunta = 0

kw_h = 0
co_2 = 0

comandos_l = ["comandos", "carbonf"]
#/////////////////////////////////////EVENTS///////////////////////////////////////
#////////////////////////////////////////////       READY       //////////////////////////////////////////////////

@bot.event
async def on_ready():
    print("  ____          ____ \n / ___|___  ___|___ \\  \n| |   / _ \\/ _ \\ __) |\n| |__|  __/ (_) / __/ \n \\____\\___|\\___/_____| \n                       ")
    print('------------------------') 
    print(f'Logged in as {bot.user}')
    print('------------------------') 
    print(f'ID: {bot.user.id}')

# //////////////////////////////////////////////         @  MENTION           ////////////////////////////////////////////////////
@bot.event
async def on_message(message):

    if bot.user in message.mentions:
        await message.channel.send(f'¡Hola {message.author.mention}! ¿En qué puedo ayudarte?')


#///////////////////////////////////////////////////////        RETURN         //////////////////////////////////

    if message.author == bot.user:
        return
    
#/////////////////////////////////////////////          COMANDO INVÁLIDO            //////////////////////////////////////////////////

    if message.content.startswith(bot.command_prefix):
        
        ctx = await bot.get_context(message)
        if ctx.invoked_subcommand is None and not ctx.command:
            
            error_message = f'Error: El comando "{message.content}" no es válido.'
            await message.channel.send(error_message)
            print(error_message) 

    await bot.process_commands(message)



#///////////////////////////////////HELP/////////////////////////////////////////////

@bot.command()
async def comandos(ctx):
    if ctx.author == bot.user:
        return

    embed = discord.Embed(
        title="COMANDOS",
        color=discord.Color.green() 
    )
    
    embed.add_field(name=f"- {comandos_l[0]}", value="Muestra una lista de todos los comandos ", inline=False)
    embed.add_field(name=f"- {comandos_l[1]}", value="El comando principal del bot, una calculadora sobre tu huella de carbono en el planeta!", inline=False)
    embed.add_field(name=f"- PROXIMAMENTE", value="Quizás un poco de información...", inline=False)

    await ctx.send(embed=embed)

    return
#/////////////////////////NEWS/////////////////////////////////

 

#///////////////////////////////CONTAMINACIÓN PROYECTO////////////////////////////

#///////////////////////            FUNCIONES              ///////////////////

#///////////////     FUNCION CO2    /////////////////////////
def co2(tipo, distancia, frecuencia):
    try:

        kg_promedio = {
            "Privado": 0.21,
            "Publico": 0.1,
        }

        dias = {
            "Diariamente": 30,  
            "Semanalmente": 4,
            "Mensualmente": 1,
        }

        tipo = tipo.capitalize()
        frecuencia = frecuencia.capitalize()

        if tipo not in kg_promedio:
            raise ValueError(f"Tipo de transporte inválido: {tipo}")
        if frecuencia not in dias:
            raise ValueError(f"Frecuencia inválida: {frecuencia}")

        distancia = float(distancia)

        return distancia * kg_promedio[tipo] * dias[frecuencia]

    except ValueError as e:
        print(f"Error en la función CO2: {e}")
        return 0
    except Exception as e:
        print(f"Error inesperado: {e}")
        return 0
    except KeyError as e:
        print("No se encontró tu información de distancia. Por favor, completa el formulario.")
        return
    except ValueError as e:
        print("La distancia guardada no es un número válido.")
        return



#///////////////     FUNCION KW/H     /////////////////////////
def kwh(num_luces, horas_por_dia = 5, dias_por_mes = 30, consumo_por_luz = 0.06):

    try:
        num_luces = int(num_luces)  
        return num_luces * horas_por_dia * dias_por_mes * consumo_por_luz
    except ValueError:
        return "Error: El número de luces debe ser un entero válido."
    

#///////////////////////////////////////////////////////////////COMANDOS////////////////////////////////////////////////////////
@bot.command()
async def carbonf(ctx):
    if ctx.author == bot.user:
        return

    if ctx.message.content.lower() == prefix + 'carbonf':
        await ctx.send(f"Bienvenido {ctx.author.mention} a la calculadora de contaminación! 🌍\nVamos a calcular tu rastro de Co2 en base a tus datos, por lo que vas a tener que rellenar un formulario.")
        time.sleep(1)

        #TRANSPORTE//////////////////////////////////////////////////////////

        await ctx.send("```🚗🚇 ¿Usas transporte público o privado?\n\nOpciones:\n🚌 - Público\n🚗 - Privado```")
        
        res1 = await bot.wait_for('message')

        transporte_bd[ctx.author.id]= res1.content
        
        with open('DB.txt', 'a', encoding='utf-8') as archivo:
            archivo.write("\nClase de Transporte: "+ res1.content)
        print(f"Transport class: ", res1.content)
        pregunta = 3
        time.sleep(2)

        if res1.content == "Privado" or res1.content == "privado":

            await ctx.send("```🚗 ¿Qué tipo de transporte usas?\n\nOpciones:\n🚗 - Automóvil\n🏍️ - Motocicleta\n🚕 - Uber```")

            res1_1 = await bot.wait_for('message')
            transporte_bd_r.append(res1_1)

            tipo_transporte_bd[ctx.author.id]= res1_1.content

            with open('DB.txt', 'a', encoding='utf-8') as archivo:
                archivo.write("\n   Tipo de Transporte: "+ res1_1.content)
            print(f"Transport type: ",res1_1.content)
            pregunta = 3
        
        #/////////////////////////////////////////////////////////////////////           PUBLICO          /////////////////////////////////////////////////////////////////////////////////////
        elif res1.content =="Publico" or res1.content == "Público" or res1.content == "publico" or res1.content == "público":

            await ctx.send("```🚌 ¿Qué tipo de transporte usas?\n\nOpciones:\n\n🚌 - Autobús\n🚂 - Tren\n🚇 - Metro\n🚊 - Tranvía\n🚕 - Taxi```")
            
            res2_1 = await bot.wait_for('message')
            transporte_bd_r.append(res2_1)


            tipo_transporte_bd[ctx.author.id]= res2_1.content

            with open('DB.txt', 'a', encoding='utf-8') as archivo:
                archivo.write("\n   Tipo de Transporte: "+ res2_1.content)
            print(f"Transport type: ",res2_1.content)
            pregunta = 3
        #////////////////////////////////////////////////////           GASTO SEGUIDO DE GASOLINA           /////////////////////////////////////////////////////////////////////////////////

        lista_transportes = ["Automovil", "Motocicleta", "Uber", "Taxi", "Tranvia", "Metro", "Tren", "Autobus", "Automóvil", "Autobús", "Tranvía", "autobus"]
        
        res2_1_1 = transporte_bd_r[0]
        if res2_1_1.content in lista_transportes:
            await ctx.send("```📍 ¿Vas a un lugar repetidas veces en el transporte?\n(Ejemplo: escuela, universidad, colegio, entre otros.)\n\nOpciones:\n✅ - Sí\n❌ - No```")
        
            res2_2 = await bot.wait_for('message')

            with open('DB.txt', 'a', encoding='utf-8') as archivo:
                archivo.write("\nLugar recurrente: "+ res2_2.content)
            print(f"Place confirmation saved as: ",res2_2.content)
            pregunta = 3
         #///////////////////////////////////////////////                      PERIODICIDAD                     ///////////////////////////////////////////////////////////////
            if res2_2.content == "Si" or res2_2.content == "Sí" or res2_2.content == "si" or res2_2.content == "sí":

                await ctx.send("```📏 Aproximadamente, ¿a qué distancia se encuentra ese lugar?\n(Introduce solo el valor, no en KM)```")
                
                res2_3 = await bot.wait_for('message')
                
                distancia_bd[ctx.author.id] = res2_3.content
                
                with open('DB.txt', 'a', encoding='utf-8') as archivo:
                    archivo.write("\n   Distancia: " + res2_3.content)
                print(f"Distance saved as: {res2_3.content}km")
                pregunta = 3

                time.sleep(1)
                
                await ctx.send("```🔁 ¿Qué tan seguido vas a ese lugar?\n\nOpciones:\n📅 - Diariamente\n📅 - Semanalmente\n📅 - Mensualmente```")

                res2_4 = await bot.wait_for('message')

                recurrencia_bd[ctx.author.id]= res2_4.content

                with open('DB.txt', 'a', encoding='utf-8') as archivo:    
                    archivo.write("\n   Periodicidad: "+ res2_4.content)    
                print(f"Periodicity saved as:",res2_4.content)
                pregunta = 3

                #////////////////////////////////////////////////               DIAS POR SEMANA               ////////////////////////////////////////////////////////////////////////////
                time.sleep(1)


                if res2_4.content == "Semanalmente":

                    await ctx.send("```🗓️ ¿Cuántos días a la semana vas?\n\nOpciones:\n1 día\n2 días\n3 días\n4 días\n5 días\n6 días\n\n Solo introduce el número de días!```")

                    res2_5 = await bot.wait_for('message')

                    por_semana_bd[ctx.author.id]= res2_5.content
                    with open('DB.txt', 'a', encoding='utf-8') as archivo:
                        archivo.write("\n       Días a la semana: "+ res2_5.content)
                    print(f"Days per week saved as: ",res2_5.content)
                    pregunta = 2


                elif res2_4.content == "Mensualmente":

                    await ctx.send("```🗓️ ¿Cuántos días al mes vas?\n(Solo introduce el número de días!)```")

                    res2_6 = await bot.wait_for('message')

                    por_mes_bd[ctx.author.id]= res2_6.content

                    with open('DB.txt', 'a', encoding='utf-8') as archivo:
                        archivo.write("\n       Días al mes: "+ res2_6.content)
                    print(f"Days per month saved as: ",res2_6.content)
                    pregunta = 2

                
                elif res2_4.content == "Diariamente":

                    await ctx.send("```🗓️ ¿Cuántos días al mes vas?\n(Solo introduce el número de días!)```")

                    res2_7 = await bot.wait_for('message')

                    por_mes_bd[ctx.author.id]= res2_7.content

                    with open('DB.txt', 'a', encoding='utf-8') as archivo:
                        archivo.write("\n       Días al mes: "+ res2_7.content)
                    print(f"Days per month saved as: ",res2_7.content)
                    pregunta = 2

            elif res2_2.content == "No" or res2_2.content == "no":
                pregunta = 2
                recurrencia_bd[ctx.author.id]= "Diariamente"
                distancia_bd[ctx.author.id] = 0
                pass
    #///////////////////////////////////////////////            ELSE            /////////////////////////////////////////////////////                
            else: 
                await ctx.send("Introduce un valor válido! ❌\n Vuelve a ejecutar el comando.")
                return
        
        else: 
            await ctx.send("Ese vehículo no existe! ❌\n Vuelve a ejecutar el comando.")
            return

        #/////////////////////////////////////////////////////////////////           CONSUMO ENERGÉTICO         ////////////////////////////////////////////////////////////////////////////

        await ctx.send(f"Perfecto {ctx.author.mention}! Ahora vamos con la sección\n**Hogar** 🏠")
        time.sleep(1)
        await ctx.send("```💡 Aproximadamente, ¿cuántas luces tienes en tu hogar?\n(Solo el número)```")
            
        res3 = await bot.wait_for('message')

        luces_bd[ctx.author.id]= res3.content
            
        with open('DB.txt', 'a', encoding='utf-8') as archivo:
                archivo.write("\nCantidad de luces: "+ res3.content)
        print(f"Lights: ", res3.content)
        pregunta = 2

        if pregunta % 2 == 0:
                
            tipo_transporte = transporte_bd[ctx.author.id]  
            distancia = float(distancia_bd[ctx.author.id]) 
            frecuencia = recurrencia_bd[ctx.author.id]     

            huella_co2 = co2(tipo_transporte, distancia, frecuencia)

            print(f"La huella de carbono estimada es: {huella_co2:.2f} kg de CO2 al mes.")
            consumo_energetico = kwh(res3.content)
            with open('DB.txt', 'a', encoding='utf-8') as archivo:
                archivo.write(f"\nConsumo Energético: {consumo_energetico} KW/h")
            print(f"Monthly Energy Consumption: {consumo_energetico} KW/h")


            emisiones_energia = int(consumo_energetico) * 0.475

            huella_total = consumo_energetico + emisiones_energia

            time.sleep(1)
            await ctx.send("🌍 Calculando tu huella de carbono....")
            time.sleep(3)

            def crear_imagen():
                plantilla = Image.open("Code\image\carbon_template.png")


                draw = ImageDraw.Draw(plantilla)
                fuente = ImageFont.truetype("arial.ttf", size=40)
                texto = f"{huella_total}\nKilogramos de Co2!"
                posicion = (280, 405)
                color_texto = (0, 0, 0)  
                draw.text(posicion, texto, fill=color_texto, font=fuente)

                plantilla.save("resultado.png")

            crear_imagen()
            embed = discord.Embed(
                title=f"Tú Huella de carbono",
                description="Aquí están los kg de tu impacto en nuestro mundo!",
                color=discord.Color.blue()
            )

            file = discord.File("resultado.png", filename="resultado.png")
            embed.set_image(url="attachment://resultado.png")

            await ctx.send(file=file, embed=embed)
    
            pregunta = 0
            user_bd.clear()
            transporte_bd.clear()
            transporte_bd_r.clear()        
            tipo_transporte_bd.clear()
            recurrencia_bd.clear()
            distancia_bd.clear()
            por_semana_bd.clear()
            por_mes_bd.clear()
            vuelos_bd.clear()
            luces_bd.clear()
            return
            time.sleep(100000)
#////////////////////////////////////////////////////////////////////////////////

bot.run(bot_token)