// pages/load/load.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    username:'', 
    password:'',
    shadow:'',
    token:''
  },

  prereguser: function() {
    wx.showModal({
      content:"请录入人脸后确定注册"
    }).then(res=>{
      if(res.confirm){
        this.reguser()
      }else if(res.cancel){
        console.log("用户点击了取消");
      }
    })
  },

  handleInputname: function(event) {
    // 将输入框的内容更新到 data 中
    this.setData({
      username: event.detail.value
    });
    console.log(this.data.username)
  },
  handleInputpassword: function(event) {
    // 将输入框的内容更新到 data 中
    this.setData({
      password: event.detail.value
    });
    console.log(this.data.password)
  },

  login() {
    const data = `username=${encodeURIComponent(this.data.username)}&password=${encodeURIComponent(this.data.password)}`;
    const username = this.data.username
    const password = this.data.password
    wx.request({
      url: 'http://121.36.40.123:8080/api/login',
      method: 'POST',
      data: data,
      header: {
        'content-type': 'application/x-www-form-urlencoded' // 默认值
      },
      success(res) {
        console.log(res);
        const message = res.data.message;
        console.log(message)
        if(res.data.status === 'ok') {
          wx.setStorageSync('username', username)
          wx.setStorageSync('password', password)
          wx.setStorageSync('height', res.data.data.height)
          wx.setStorageSync('weight', res.data.data.weight)
          wx.setStorageSync('bmi', res.data.data.BMI)
          wx.setStorageSync('cash', res.data.data.cash)
          console.log(res.data.data.plan)
          wx.setStorageSync('faceid', res.data.data.plan)
          wx.setStorageSync('age', res.data.data.age)
          wx.setStorageSync('gender', res.data.data.gender)
          wx.showToast({
            title: "登入成功！",
            icon: 'none',
            duration: 2000 
          });
          wx.redirectTo({
            url: '/pages/me/me' // 跳转到“我”界面
          });
        }
        else if(message.includes('"username" is not allowed to be empty')) {
          wx.showToast({
            title: "用户名不能为空！",
            icon: 'none', 
            duration: 2000 
          });
        }
        else if(message.includes('"password" is not allowed to be empty')) {
          wx.showToast({
            title: "密码不能为空！",
            icon: 'none', 
            duration: 2000 
          });
        }
        else if(message.includes('登入失败！')) {
          wx.showToast({
            title: "登入失败！",
            icon: 'none', 
            duration: 2000 
          });
        }
      },
    });
  },

  reguser() {
    console.log(this.data.token)
    var shadow;
    wx.request({
      url: 'https://iotda.cn-north-4.myhuaweicloud.com/v5/iot/669de7f3752c794e18d20b60/devices/669de7f3752c794e18d20b60_berry1/shadow',
      method: 'GET',
      header: {'content-type': 'application/json', 'X-Auth-Token':this.data.token},
      success: (res) => {
          console.log(res)
          shadow=JSON.stringify(res.data.shadow[0].reported.properties.faceID)
          console.log('设备影子数据：'+shadow);
          this.setData({
            shadow: shadow
          })
          const data = `username=${encodeURIComponent(this.data.username)}&password=${encodeURIComponent(this.data.password)}&plan=${encodeURIComponent(this.data.shadow)}`;
          console.log(data)
          wx.request({
            url: 'http://121.36.40.123:8080/api/reguser',
            method: 'POST',
            data: data,
            header: {
              'content-type': 'application/x-www-form-urlencoded' // 默认值
            },
            success(res) {
              console.log(res);
              const message = res.data.message;
              console.log(message)
              if(message.includes('用户名已被占用')) {
              wx.showToast({
                title: "用户名已被占用！",
                icon: 'none', 
                duration: 2000 
              });
            }
            else if(message.includes('"username" is not allowed to be empty')) {
              wx.showToast({
                title: "用户名不能为空！",
                icon: 'none', 
                duration: 2000 
              });
            }
            else if(message.includes('"password" is not allowed to be empty')) {
              wx.showToast({
                title: "密码不能为空！",
                icon: 'none', 
                duration: 2000 
              });
            }   
            else if(message.includes('"password" length must be at least 6 characters long')) {
              wx.showToast({
                title: "密码过短！",
                icon: 'none', 
                duration: 2000 
              });
            }
            else if(message.includes('"password" length must be less than or equal to 12 characters long')) {
              wx.showToast({
                title: "密码过长！",
                icon: 'none', 
                duration: 2000 
              });
            }
            else if(message.includes('注册成功！')) {
              wx.showToast({
                title: "注册成功！",
                icon: 'none', 
                duration: 5000 
              });
            }
          }
        })
      }
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    wx.request({
      url: 'https://iam.cn-north-4.myhuaweicloud.com/v3/auth/tokens',
      method: 'POST',
      header: {'Content-Type': 'application/json'},
      data: {
          "auth": {
              "identity": {
                  "methods": [
                      "password"
                  ],
                  "password": {
                      "user": {
                          "name": "qqqb",
                          "password": "wan13688007964",
                          "domain": {
                              "name": "hid_nh5y032_-g3izl8"
                          }
                      }
                  }
              },
              "scope": {
                  "project": {
                      "name": "cn-north-4"
                  }
              }
          },
      },
      success: (res) => {
          //console.log(res)
          this.setData ({
              token: res.header['X-Subject-Token']
          })
      }
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