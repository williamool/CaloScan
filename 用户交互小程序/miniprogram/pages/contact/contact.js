// pages/contact/contact.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    // 用户信息
    userInfo: {},
    // 判断显示授权前或授权后的样式
    hasUserInfo: false
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
    // 获取存储的用户授权信息
    const userinfo =  wx.getStorageSync('userinfo') || {}
    console.log(Object.keys(userinfo));
    // 判断是否存在已经授权的用户信息
    if (Object.keys(userinfo).length == 0) {
      this.setData({
        userInfo: userinfo,
        hasUserInfo: false
      })
    } else {
      this.setData({
        userInfo: userinfo,
        hasUserInfo: true
      })
    }
  },

  getUserProfile(e) {
    let that = this
    // 获取个人信息
    wx.getUserProfile({
      desc: '用于获取用户个人信息',
      success: function (detail) {
        console.log(detail);
        wx.login({
          success: res => {
            var code = res.code; //登录凭证
            wx.request({
              url: 'http://127.0.0.1:8888/api/wxuser', //自己的服务接口地址
              method: 'post',
              header: {
                'content-type': 'application/x-www-form-urlencoded'
              },
              // 需要传给后端的数据
              data: {
                encryptedData: detail.encryptedData,
                iv: detail.iv,
                code: code,
                userInfo: detail.rawData

              },
              success: (res) => {
                console.log("res:", res.data)
                // 将用户授权信息存储到本地
                wx.setStorageSync('userinfo', detail.userInfo)
                // 将后端返回的token存储到本地
                wx.setStorageSync('token', res.data.token)
                that.setData({
                  userInfo: detail.userInfo,
                  hasUserInfo: true
                })
              },
              fail: function () {
                console.log('系统错误')
              }
            })
          }
        });
      },
      fail: function () {
       wx.showModal({
         content: '取消授权将会影响相关服务，您确定取消授权吗？',
         success (res) {
           if (res.confirm) {
             wx.showToast({
               title: '已取消授权',
               duration: 1500
             })
           } else if (res.cancel) {
             that.getUserProfile()
           }
         }

       })
      }
    })
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