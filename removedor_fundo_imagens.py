import os
from PIL import Image

#Remove fundo branco de imagens com tipo .jpg de uma pasta escolhida pelo usuário


pasta = input("Escolha a pasta de entrada: ")

for nome_arquivo in os.listdir(pasta):
    if nome_arquivo.endswith('.jpg'):
        caminho_arquivo = os.path.join(pasta, nome_arquivo)
        
        imagem = Image.open(caminho_arquivo).convert("RGBA")
        
        nova_imagem = Image.new("RGBA", imagem.size)
        largura, altura = imagem.size
        
        for x in range(largura):
            for y in range(altura):
                r, g, b, a = imagem.getpixel((x, y))

                if r > 240 and g > 240 and b > 240:  
                    nova_imagem.putpixel((x, y), (255, 255, 255, 0))
                else:
                    nova_imagem.putpixel((x, y), (r, g, b, a))
        
        nova_imagem.save(caminho_arquivo, 'PNG')

print("Processo concluído: fundo removido de todas as imagens JPG.")
