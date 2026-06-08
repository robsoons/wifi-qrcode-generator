# wifi-qrcode-generator
Aplicação em Python para gerar QR Codes de redes Wi-Fi através de interface gráfica.
--------------------------- #
# Gerador de QR Code Wi-Fi #

Script em Python para gerar QR Code de rede Wi-Fi com base em SSID e senha, com opcao de incluir logo da empresa no centro.

Agora voce pode usar por linha de comando ou pela interface grafica.

## 1) Instalar dependencias

No terminal, dentro desta pasta:

```powershell
pip install -r requirements.txt
```

## 2) Uso basico (sem logo)

```powershell
python gerar_qrcode_wifi.py --ssid "MinhaRede" --password "MinhaSenha123" --security WPA --output "wifi_sem_logo.png"
```

## Interface grafica (modo recomendado para editar sempre)

```powershell
python interface_qrcode_wifi.py
```

Na interface, voce preenche os campos e clica em `Gerar QR Code`.

Ou execute com duplo clique no arquivo:

- `ABRIR_INTERFACE_QRCODE.bat`

## 3) Uso com logo da empresa

```powershell
python gerar_qrcode_wifi.py --ssid "MinhaRede" --password "MinhaSenha123" --security WPA --logo "logo_empresa.png" --output "wifi_com_logo.png"
```

## 4) Rede aberta (sem senha)

```powershell
python gerar_qrcode_wifi.py --ssid "RedeVisitantes" --security nopass --output "wifi_aberta.png"
```

## Parametros

- `--ssid` (obrigatorio): nome da rede Wi-Fi
- `--password`: senha da rede
- `--security`: `WPA`, `WEP` ou `nopass`
- `--hidden`: marque se a rede for oculta
- `--output`: caminho do arquivo PNG de saida
- `--logo`: caminho para imagem do logo (png/jpg)
- `--logo-scale`: tamanho relativo do logo (padrao 0.20)
- `--box-size`: tamanho de cada bloco do QR (padrao 10)
- `--border`: borda do QR em blocos (padrao 4)
- `--fill-color`: cor do QR
- `--back-color`: cor de fundo

## Dica

Se usar logo, mantenha `--logo-scale` entre `0.10` e `0.25` para melhor leitura por celular.
