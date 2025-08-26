// pages/imageinfo/imageinfo.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    weiliang:'',
    yinyang:'',
    weisheng:'',
    zhexian:'',
    zhuzhuang:'',
    faceid: 0,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    var faceid = wx.getStorageSync('faceid')
    const formattedMonth = wx.getStorageSync('month')
    const formattedDay = wx.getStorageSync('day')
    console.log(formattedDay)
    const weiliang = `https://obs1111112.obs.cn-north-4.myhuaweicloud.com/test_今日基本微量元素摄入量_day2024-${formattedMonth}-${formattedDay}_id${faceid}.png`;
    const weisheng = `https://obs1111112.obs.cn-north-4.myhuaweicloud.com/test_今日基本维生素摄入量_day2024-${formattedMonth}-${formattedDay}_id${faceid}.png`;
    const yinyang = `https://obs1111112.obs.cn-north-4.myhuaweicloud.com/test_今日基本营养素摄入量_day2024-${formattedMonth}-${formattedDay}_id${faceid}.png`;
    const zhuzhuang = `https://obs1111112.obs.cn-north-4.myhuaweicloud.com/test_七日营养素柱状图_day2024-${formattedMonth}-${formattedDay}_id${faceid}.png`;
    const zhexian = `https://obs1111112.obs.cn-north-4.myhuaweicloud.com/test_七日历史饮食记录_day2024-${formattedMonth}-${formattedDay}_id${faceid}.png`;

    this.setData ({
      weiliang: weiliang,
      weisheng: weisheng,
      yinyang: yinyang,
      zhuzhuang: zhuzhuang,
      zhexian: zhexian
    })
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