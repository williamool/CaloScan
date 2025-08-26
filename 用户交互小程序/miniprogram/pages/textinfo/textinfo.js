// pages/textinfo/textinfo.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    filecontent:''
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    
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
    const formattedMonth = wx.getStorageSync('month')
    const formattedDay = wx.getStorageSync('day')
    console.log(formattedDay)
    var faceid = wx.getStorageSync('faceid')
    const txt = `https://obs1111112.obs.cn-north-4.myhuaweicloud.com/test_当日饮食建议_day2024-${formattedMonth}-${formattedDay}_id${faceid}.txt`;
    console.log(txt)

    wx.downloadFile({
      url: txt,
      success: (res) => {
        console.log(1)
        if(res.tempFilePath) {
          wx.getFileSystemManager().readFile({
            filePath: res.tempFilePath,
            success: (res) => {
              const content = res.data;
              console.log(1)
              console.log(content)
              const uint8Array = new Uint8Array(content)
              const decodedString = decodeURIComponent(escape(String.fromCharCode(...uint8Array)))
              console.log(decodedString); // 打印转换后的字符串
              this.setData({ fileContent: decodedString });
            }
          })
        }
      }
    })
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