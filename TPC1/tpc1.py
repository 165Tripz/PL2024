import re

# Abrir o ficheiro
emd_csv = open("emd.csv")

# Iremos assumir que as colunas serão sempre as mesmas para requisitar os valores

colunas = re.compile(r'[^,]*,[^,]*,[^,]*,[^,]*,[^,]*,(?P<age>[^,]*),[^,]*,[^,]*,(?P<mod>[^,]*),[^,]*,[^,]*,[^,]*,(?P<res>true|false)',re.I|re.X)
binning = re.compile(r'(?P<F>[1-9])((?P<B04>[0-4])|(?P<B59>[5-9]))')

# Ignorar a primeira linha da coluna
emd_csv.readline()

dicionario_binning_idades = {}
for i in range(1,10):
    dicionario_binning_idades.update({str(i)+'0-'+str(i)+'4':0, str(i)+'5-'+str(i)+'9':0})
dicionario_binning_mods = {}
lista_aptidao = [0,0]
dicionario_aptidao = dict()

for line in emd_csv:
    result = colunas.match(line)
    bin_result = binning.match(result.group('age'))
    modalidade = result.group('mod')
    
    if bin_result.group('F') != None:
        if dicionario_binning_mods.get(modalidade) == None:
            dicionario_binning_mods[modalidade] = {}
            for i in range(1,10):
                dicionario_binning_mods[modalidade].update({str(i)+'0-'+str(i)+'4':0, str(i)+'5-'+str(i)+'9':0})
        first_num = bin_result.group('F')
        if bin_result.group('B04') != None:
            dicionario_binning_idades[first_num + '0-' + first_num + '4']  += 1
            dicionario_binning_mods[modalidade][first_num + '0-' + first_num + '4']  += 1
        elif bin_result.group('B59') != None:
            dicionario_binning_idades[first_num + '5-' + first_num + '9']  += 1
            dicionario_binning_mods[modalidade][first_num + '5-' + first_num + '9']  += 1
    
    if dicionario_aptidao.get(modalidade) == None:
        dicionario_aptidao[modalidade] = [0,0]
    
    if result.group('res') == 'true':
        lista_aptidao[0] += 1
        dicionario_aptidao[modalidade][0] +=1
    
    elif result.group('res') == 'false':
        dicionario_aptidao[modalidade][1] +=1
        lista_aptidao[1] += 1

lista_modalidades = list(dicionario_aptidao.keys())
lista_modalidades.sort()

print()

print('Lista Ordenada de Modalidades:')
for item in lista_modalidades:
    print('- ' + item)

print()
for key, lista in dicionario_aptidao.items():
    (i1,i2) = tuple(lista)
    print(f'{key} tem {i1*100/(i1+i2):.2f}% atletas aptos e {i2*100/(i1+i2):.2f}% atletas inaptos.')

print()

(i1,i2) = tuple(lista_aptidao)
print(f"No total {i1*100/(i1+i2):.2f}% dos atletas estão aptos e {i2*100/(i1+i2):.2f}% estão inaptos.")

print()

print('Distribuição de atletas por escalão etário:')
for key, num in dicionario_binning_idades.items():
    if num != 0:
        print(f"- [{key}] : {num}")

print()

print('Distribuição de atletas por escalão etário e por desporto:')
for mod, dict2 in dicionario_binning_mods.items():
    print(f'\nEm {mod}:')
    for key, num in dict2.items():
        if num != 0:
            print(f"- [{key}] : {num}")
