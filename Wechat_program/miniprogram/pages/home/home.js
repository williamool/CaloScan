// pages/home/home.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    token: '',
    types: 0,
    dishName: '',
    cleanweight:0,
    temp:0,
    flag: -1,
    username: '',
    time: '',
    dishid: [],
    weight: [],
    price: [],
    totalprice: 0,
  },

  //获取当日菜品信息
  get_daily_dish: function(types) {
    const dishes = {
      "0": "蒸排骨",
      "1": "鱼香肉丝",
      "2": "宫保鸡丁",
      "3": "水煮牛肉",
      "4": "番茄牛腩",
      "5": "萝卜牛腩",
      "6": "红烧猪蹄",
      "7": "萝卜炖排骨",
      "8": "咕噜肉",
      "9": "青椒土豆丝",
      "10": "地三鲜",
      "11": "京酱肉丝",
      "12": "孜然羊肉",
      "13": "土豆炖牛肉",
      "14": "紫菜蛋花汤",
      "15": "干锅排骨",
      "16": "油渣炒莲白",
      "17": "白切鸡",
      "18": "南瓜粥",
      "19": "蒸饺",
      "20": "莲白粉丝",
      "21": "莲藕排骨汤",
      "22": "酱油炒饭",
      "23": "苦瓜炒肉",
      "24": "清炒上海青",
      "25": "番茄鸡蛋汤",
      "26": "菠萝炒饭",
      "27": "红烧鱼",
      "28": "剁椒茄子",
      "29": "蒜香排骨",
      "30": "担担面",
      "31": "白灼西兰花",
      "32": "红糖糍粑",
      "33": "清蒸鲈鱼",
      "34": "红烧狮子头",
      "35": "青椒肉丝",
      "36": "毛血旺",
      "37": "啤酒鱼",
      "38": "红油饺子",
      "39": "青椒小炒肉",
      "40": "酸菜粉丝汤",
      "41": "青菜豆腐汤",
      "42": "麻婆豆腐",
      "43": "梅菜扣肉",
      "44": "青椒炒蛋",
      "45": "干锅花菜",
      "46": "凉拌黄瓜",
      "47": "韭黄炒蛋",
      "48": "芋头蒸排骨",
      "49": "蟹黄豆腐",
      "50": "蒜蓉菜心",
      "51": "干煸兔丁",
      "52": "蒜蓉虾",
      "53": "玉米排骨汤"
    }
    const currentDate = new Date();
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth() + 1; 
    const day = currentDate.getDate();
    const formattedMonth = String(month).padStart(2, '0');
    const formattedDay = String(day).padStart(2, '0');
    var time = year + formattedMonth + formattedDay
    this.setData ({
      time: time
    })
    const data = `username=${encodeURIComponent(this.data.username)}&time=${encodeURIComponent(this.data.time)}`;
    wx.request({
      url: 'http://121.36.40.123:8080/api/get_daily_dish',
      method: 'POST',
      data: data,
      header: {
        'content-type': 'application/x-www-form-urlencoded' // 默认值
      },
      success: (res) => {
        let dishid = [];
        let weight = [];
        let price = [];
        var answer = res.data.data.results
        var totalprice = 0;
        console.log(answer)
        answer.forEach((item) => {
          dishid.push(dishes[item.dishid])
          weight.push(item.weight)
          price.push(item.price)
          totalprice += item.price
        });
        this.setData ({
          dishid: dishid,
          weight: weight,
          price: price,
          totalprice: totalprice.toFixed(2)
        })
      }
    })
  },
    //获取token
  getToken() {
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
            wx.setStorageSync('token', this.data.token)
            //console.log("token为："+token)
        }
      })
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    var username = wx.getStorageSync('username')
    this.setData ({
      username: username
    })
    if(username === '') {
      wx.showToast({
        title: "请先登入！",
        icon: 'none',
        duration: 10000
      });
    }
    else this.get_daily_dish()
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