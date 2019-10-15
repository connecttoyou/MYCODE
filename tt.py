import os,sys,time,asyncio,aiohttp,io
import tqdm

class DownLoad(object):
    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def savepath(self):
        return self._savepath

    @savepath.setter
    def savepath(self, value):
        self._savepath = value

    # FLAGS = ('CN IN US ID BR PK NG BD RU JP '
    #      'MX PH VN ET EG DE IR TR CD FR').split()

    def _save_file_(self,fd:io.BufferedWriter,chunk):
        fd.write(chunk)


    async def _fetch_(self,session:aiohttp.ClientSession):
        print(' 开始下载')
        async with session.get(self.url) as resp:
           with open(self.savepath,'wb') as fd:
                while 1:
                    chunk = await resp.content.read(8192)
                    if not chunk:
                        break
                    lp = asyncio.get_event_loop()
                    lp.run_in_executor(None,self._save_file_,fd,chunk)
                    # fd.write(chunk)
                fd.close()

    # async def __fetch__(session:aiohttp.ClientSession,url:str,path:str,flag:str):
    #     print(flag, ' 开始下载')
    #     async with session.get(url) as resp:
    #         with open(path,'wb') as fd:
    #             while 1:
    #                 chunk = await resp.content.read(1024)    #每次获取1024字节
    #                 if not chunk:
    #                     break
    #                 fd.write(chunk)
    #     return flag

    async def _begin_download_(self,sem,session:aiohttp.ClientSession):    #控制协程并发数量
        async with sem:
            return await self._fetch_(session)

    async def _download_(self,sem:asyncio.Semaphore):
        tasks = []
        try:
            async with aiohttp.ClientSession() as session:
                # for flag in self.FLAGS:            #创建路径以及url
                #    path = os.path.join(self.savepath, flag.lower() + '.gif')
                #    url = '{}/{cc}/{cc}.gif'.format(self.url, cc=flag.lower())
                   #构造一个协程列表
                   tasks.append(asyncio.ensure_future(self._begin_download_(sem,session)))
                   #等待返回结果
                   tasks_iter = asyncio.as_completed(tasks)
                   #创建一个进度条
                   fk_task_iter = tqdm.tqdm(tasks_iter,total=len(self.FLAGS))
                   for coroutine in fk_task_iter:
                        #获取结果
                        res = await coroutine
                        print(res, '下载完成')
        except:
            with Exception as ex:
                print(ex)

    def run(self):
        #创建目录
        os.makedirs(self.savepath,exist_ok=True)
        #获取事件循环
        lp = asyncio.get_event_loop()
        start = time.time()
         #创建一个信号量以防止DDos
        sem = asyncio.Semaphore(4)
        lp.run_until_complete(self._download_(sem))
        end = time.time()
        lp.close()
        print('耗时:',end-start)


dl=DownLoad()
dl.url='http://flupy.org/data/flags'
dl.savepath= 'f://downloads//'
dl.run()