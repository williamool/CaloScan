// pages/message/message.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    step:null,
    isSelect:false,//展示类型？
    types:[],//公司/商户类型
    type:"",
    swiperList: [],
    hot:0,
    month:'',
    day:'',
    username: '',
    faceid: '',
    status: '',
  },

  refresh_data() {
    const data = `faceid=${encodeURIComponent(this.data.faceid)}`;
    wx.request({
      url: 'http://121.36.40.123:8080/api/getnutri',
      method: 'POST',
      data: data,
      header: {
        'content-type': 'application/x-www-form-urlencoded' // 默认值
      },
      success(res) {
        console.log(res)
      }
    })
    wx.showToast({
      title: "正在分析您的饮食数据...",
      icon: 'none', 
      duration: 5000
    });
  },

  gotoinfo() {
    if(this.data.type === "") {
      wx.showToast({
        title: "请选择统计日期！",
        icon: 'none', 
        duration: 2000 
      });
    }
    else {
      const match = this.data.type.match(/(\d{1,2})日/);
      const day = match ? match[1] : null;
      const formattedMonth = this.data.month < 10 ? `0${this.data.month}` : this.data.month;
      const formattedDay = day < 10 ? `0${day}` : day;
      wx.setStorageSync('month', formattedMonth)
      wx.setStorageSync('day', formattedDay)
      console.log(formattedMonth)
      console.log(formattedDay)
      wx.navigateTo({
        url: '/pages/imageinfo/imageinfo', 
        success: function(res) {
          console.log('获取成功')
        },
      })
    }
  },

  getacc() {
    if(this.data.type === "") {
      wx.showToast({
        title: "请选择统计日期！",
        icon: 'none', 
        duration: 2000 
      });
    }
    else {
      wx.navigateTo({
        url: '/pages/textinfo/textinfo', 
        success: function(res) {
          console.log('获取成功')
        },
      })
    }
  },

  //点击控制下拉框的展示、隐藏
  select:function(){
    var isSelect = this.data.isSelect
    this.setData({ isSelect:!isSelect})
  },
  //点击下拉框选项，选中并隐藏下拉框
  getType:function(e){
    let value = e.currentTarget.dataset.type
    this.setData({
      type:value ,
      isSelect: false,
    })
    console.log(this.data.type)
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    var that = this;
    wx.login({
      success:function(resLonin){
        console.log(resLonin)
        console.log("登入code为:",resLonin.code)
        wx.cloud.init({
            env: 'cloud1-6gqzqeqf2f9ed446'
        })  
        wx.getWeRunData({
          success:function(resRun){
            console.log("微信运动密文：")
            console.log(resRun) 
            wx.cloud.callFunction({
              name:'weRun',//云函数的文件名
              data:{
                weRunData: wx.cloud.CloudID(resRun.cloudID),
                obj:{
                  shareInfo: wx.cloud.CloudID(resRun.cloudID)
                }
              },
              success: function (res) {
                console.log("云函数接收到的数据:")
                console.log(res)
                let step = res.result.event.weRunData.data.stepInfoList[30].step
                var status = ''
                if(step < 5000) {
                  status = '运动较少'
                }
                else if(step >= 5000 && step < 10000) {
                  status = '运动适量'
                }
                else status = '运动积极'
                wx.setStorageSync('step', step)
                that.setData({
                  step:step,
                  status:status
                })
                console.log("得到的今日步数：",that.data.step)
                that.setData ({
                    hot: (0.00076 * step * 60).toFixed(0),
                })
              }
            })
          }
        })
      }
    })

    var username = wx.getStorageSync('username')
    var faceid = wx.getStorageSync('faceid')
    this.setData ({
      username: username,
      faceid: faceid
    })
    if(username === '') {
      wx.showToast({
        title: "请先登入！",
        icon: 'none',
        duration: 10000
      });
    }
  },


  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {
    const systemInfo = wx.getSystemInfoSync();
    const currentDate = new Date();
    const month = currentDate.getMonth() + 1; 
    const day = currentDate.getDate();
    const newDates = [
      `${month}月${day}日`,
      `${month}月${day - 1}日`,
      `${month}月${day - 2}日`
    ];
    this.setData({
      month: month,
      day: day,
      types: newDates
    });
    const formattedMonth = this.data.month < 10 ? `0${this.data.month}` : this.data.month;
    const formattedDay = day < 10 ? `0${day}` : day;
    wx.setStorageSync('month', formattedMonth)
    wx.setStorageSync('day', formattedDay)
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {
    
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {

  }
})