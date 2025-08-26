# 引入模块
from obs import ObsClient
# 创建ObsClient实例
obsClient = ObsClient(
    access_key_id='UXC42LP5RRWVWSCHBWRT',
    secret_access_key='W80HelKVRo4Gdpc93rWLPbnPnJGdT00Eb6MOtgg7',
    server='obs.cn-north-4.myhuaweicloud.com'
)


# 使用访问OBS

try:
    resp = obsClient.getObject(
	    	'obs1111112',
	    	'62.jpg',
	    	downloadPath='./test.jpg'
    	)

    if resp.status < 300:
        print('requestId:', resp.requestId)
        print('url:', resp.body.url)
    else:
        print('errorCode:', resp.errorCode)
        print('errorMessage:', resp.errorMessage)
except:
    import traceback

    print(traceback.format_exc())

# 关闭obsClient
obsClient.close()
