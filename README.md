#自用，都是大佬的作品，我只是借鉴

#青龙面板拉取

docker run -dit \
-v /root/ql/config:/ql/config \
-v /root/ql/log:/ql/log \
-v /root/ql/db:/ql/db \
-v /root/ql/scripts:/ql/scripts \
-v /root/ql/jbot:/ql/jbot \
-v /root/ql/repo:/ql/repo \
-p 5700:5700 \
-e ENABLE_HANGUP=true \
-e ENABLE_WEB_PANEL=true \
--name ql \
--hostname ql \
--privileged=true \
--restart always \
whyour/qinglong:2.10.13
