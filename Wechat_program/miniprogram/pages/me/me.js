// pages/me/me.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    tempweight:'',
    tempheight:'',
    username:'',
    userheight:"",
    userweight:"",
    userbmi:'',
    userplan:'',
    isSelect:false,//展示类型？
    BMI:0,
    status:"",
    cash: 0,
    sex: [{
      id: 1,
      value: '男'
    }, {
      id: 2,
      value: '女'
    }],
    Sex: '',
    age: '',
  },

  // sexinp
  radioChange: function (e) {
    // console.log('radio发生change事件，携带value值为：', e.detail.value)
    const sex = this.data.sex
    for (let i = 0, len = sex.length; i < len; ++i) {
      sex[i].checked = sex[i].id == e.detail.value
    }
    this.setData({
      Sex:e.detail.value,
      sex
    })
    console.log(this.data.sex);
  },
  postaddManage: function () {
    let sex = '';
    this.data.sex.map((item, index) => {
      if (item.checked) {
        sex = item.id;
      }
    })
    let params = {
        sex: sex,
    }
    addManage(params).then(res => {
        console.log(res);
    })
  },

  calculate: function() {
    var height = this.data.tempheight;
    var weight = this.data.tempweight;
    var bmi = (weight / (height * height / 10000)).toFixed(2);
    const step = wx.getStorageSync('step')
    console.log(step)
    const data = `username=${encodeURIComponent(this.data.username)}&weight=${encodeURIComponent(this.data.tempweight)}&height=${encodeURIComponent(this.data.tempheight)}&bmi=${encodeURIComponent(bmi)}&gender=${encodeURIComponent(this.data.Sex)}&age=${encodeURIComponent(this.data.age)}&step=${encodeURIComponent(step)}`;
    wx.request({
      url: 'http://121.36.40.123:8080/api/personinfo',
      method: 'POST',
      data: data,
      header: {
        'content-type': 'application/x-www-form-urlencoded' // 默认值
      },
      success: (res) => {
        console.log(bmi)
        this.setData ({
          BMI: bmi,
          userheight: this.data.tempheight,
          userweight: this.data.tempweight,
        })
        if(bmi < 18.5) {
          this.setData ({
              status: '体重过低'
          })
        }
        else if(bmi >= 18.5 && bmi < 24) {
          this.setData ({
              status: '正常'
          })
        }
        else if(bmi >= 24 && bmi < 28) {
          this.setData ({
              status: '超重'
          })
        }
        else {
          this.setData ({
              status: '肥胖'
          })
        }
      }
    })
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad() {
    const username = wx.getStorageSync('username')
    const weight = wx.getStorageSync('weight')
    const height = wx.getStorageSync('height')
    const bmi = wx.getStorageSync('bmi')
    const cash = wx.getStorageSync('cash')
    const age = wx.getStorageSync('age')
    const gender = wx.getStorageSync('gender')
    console.log(gender)
    console.log(bmi)
    this.setData({
      username: username,
      userweight: weight,
      userheight: height,
      BMI: bmi,
      cash: cash,
      age: age,
      Sex: gender,
    })
    const sex = this.data.sex
    for (let i = 0, len = sex.length; i < len; ++i) {
      if(sex[i].id === this.data.Sex) {
        console.log()
        sex[i].checked = true
      }
    }
    this.setData({
      sex
    })
    console.log(this.data.sex)
    if(bmi < 18.5) {
      this.setData ({
          status: '体重过低'
      })
    }
    else if(bmi >= 18.5 && bmi < 24) {
      this.setData ({
          status: '正常'
      })
    }
    else if(bmi >= 24 && bmi < 28) {
      this.setData ({
          status: '超重'
      })
    }
    else {
      this.setData ({
          status: '肥胖'
      })
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
  onShow(){
    
  },

  userheight:function(options) {
    let value = options.detail.value;
    this.setData({
        tempheight: value
    })
    console.log(this.data.tempheight);
  },
  userweight:function(options) {
      let value = options.detail.value;
      this.setData({
          tempweight: value
      })
      console.log(this.data.tempweight);
  },
  userage:function(options) {
    let value = options.detail.value;
    this.setData({
      age: value
    })
    console.log(this.data.age)
  },

  //退出登录
  exit(){
    wx.showModal({
      content:"确定退出吗"
    }).then(res=>{
      if(res.confirm){
      console.log("用户点击了确定");
      wx.clearStorageSync();
      wx.redirectTo({
        url: '/pages/load/load',
      })
      }else if(res.cancel){
        console.log("用户点击了取消");
      }
    })
  },

  //点击控制下拉框的展示、隐藏
  select:function(){
    var isSelect = this.data.isSelect
    this.setData({ isSelect:!isSelect})
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