# coding:utf-8

class Pagination:
    def __init__(self, p, all_count, pre=10, max_show=11):
    '''
    :param p: 当前页码
    :param all_count: 数据总条数
    :param pre: 每页数据量
    :param max_show: 最多页码数
    '''
    try:
    self.p = int(p)  # 传进来的页码
    if self.p <= 0:
    self.p = 1
  except Exception as e:
  self.p = 1
  
  # 总量
  # all_count = all_count
  # pre = per # 每页数据条数
  total_num, more = divmod(all_count, pre)
  if more:
  total_num += 1  # total_num总数据页数
  
  # 显示页码数
  max_show = max_show
  if total_num <= max_show: # 总数据量很小
  page_start = 1
  page_end = total_num
  else:
   if self.p - max_show // 2 <= 0:  # 防止左边出现0页
  page_start = 1
  page_end = max_show
  
  elif self.p + max_show // 2 >= total_num + 1: # 防止右边出现超出
  page_end = total_num
  page_start = page_end - max_show
  else:
  page_start = self.p - max_show // 2
  page_end = self.p + max_show // 2
  
  # 数据的起始结束
  self.start = (self.p - 1) * pre
  self.end = self.p * pre
  
  # 页码
  self.page_start = page_start
  self.page_end = page_end
  self.total_num = total_num
  
  @property
  def page_html(self):
  li_list = []
  for i in range(self.page_start, self.page_end + 1):
   if i == self.p:
  li_list.append('<li class="active"><a href="?p={}" >{}</a></li>'.format(i, i))
  else:
  li_list.append('<li><a href="?p={}" >{}</a></li>'.format(i, i))
  
  # 添加页首 页尾
  
  li_list.insert(0,
                 '<li><a href="?p={}" aria-label="Previous"><span aria-hidden="true">«</span></a></li>'.format(
                     self.p - 1))
  li_list.append(
    '<li><a href="?p={}" aria-label="Next"><span aria-hidden="true">»</span> </a></li>'.format(self.p + 1))
  
  if self.p == 1:
  li_list[0] = '<li class="disabled"><span aria-hidden="true">«</span></li>'
  elif self.p == self.total_num:
  li_list[-1] = '<li class="disabled"><span aria-hidden="true">»</span></li>'
  
  pagehtml = ''.join(li_list)
  return pagehtml


print(Pagination(1,100))
