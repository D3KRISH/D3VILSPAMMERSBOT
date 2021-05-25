# Thanks to mkaraniya & D3KRISH

FROM fusuf/asenauserbot:latest
RUN git clone https://github.com/D3KRISH/D3VILSPAMMERSBOT /root/AsenaUserBot
WORKDIR /root/AsenaUserBot/
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"]  
