# waiterian-line-bot

## 設計理念

每當到了晚餐時間，飢腸轆轆的你是否不知道要吃甚麼呢? 這個困難的問題就交給waiterian來當你想吧!

**waiterian**這個linebot提供兩個主要的服務，分別是

* `搜索附近的餐廳`
透過篩選器，選擇**位置**、**搜索半徑**、**價錢標準**和**關鍵字**，waiterian就會幫你搜尋符合條件並且正在營業的店家，並提供google的星數、地址、圖片等訊息，方便你選擇想要吃的餐廳!

* `搜索各類的食譜`
餐餐外食也會有吃膩或是有健康上的負擔，這時候親自下廚往往是最好的選擇，這時候waiterian可以提供各類的食譜，像是**點心**、**家常料理**、**異國料理**、**冰品與飲品**等，你只要選擇你喜歡的食譜然後跟著食譜一步一步動手做就可以了喔!

希望透過這些服務可以幫助每個人解決吃飯的困擾


## 基本資訊

加入waiterian-line-bot的連結 -> [點我](https://liff.line.me/1645278921-kWRPP32q/?accountId=219dhddi)
<p align="center">
	<img src="https://i.imgur.com/MZ2Kkkd.png"  width="500">
</p>


## 使用說明

### 主選單
輸入`waiterian`可以叫出主選單，或是直接使用圖文選單的主選單也可以
<p align="center">
	<img src="https://i.imgur.com/3YJWrpK.png"  width="500">
</p>

### 搜尋餐廳
點選`RESTAURANR`的圖標，state轉換為`search_restaurant`，並跳出搜尋餐廳的**篩選器**


透過點擊篩選器的按鈕可以修改設定的值，下列幾點需要注意

* 預設的設定值會是上次搜尋的設定值
* 每當開始設定，需要完成數值的設定後才能繼續下個設定
    * e.g. 當選位置訊息時，state轉換為`get_location`，使用者需要輸入位置使state轉換為`search_restaurant`，才能既須接下來的設定
* 設定時，需要以`>> `作為前綴並輸入正確的值機器人才能順利設定
    * e.g. 在設定關鍵字時，可以使用`>> 日式`來搜尋特定種類的餐廳
* 搜尋結束時，需要使用`QUIT`離開當前狀態使state轉換為`idle`

<p align="center">
	<img src="https://i.imgur.com/zYcZ7m3.png"  width="500">
</p>

<p align="center">
	<img src="https://i.imgur.com/omT55VA.jpg"  width="500">
</p>

#### 搜尋結果
<p align="center">
	<img src="https://i.imgur.com/zlqKneE.jpg"  width="500">
</p>

<p align="center">
	<img src="https://i.imgur.com/AbGRfr1.png"  width="500">
</p>

<p align="center">
	<img src="https://i.imgur.com/mWk82D7.jpg"  width="500">
</p>



### 搜尋食譜

點選`RECIPE`的圖標，state轉換為`search_recipe`，並跳出各種不同**種類**的按鈕

當按下某個**種類**的按鈕時，會顯示該種類的**細項**，此時選擇你想要的細項點擊後，就會產生該細項的食譜。

有幾點事情需要注意
* 顯示細項時會進入該種類的state，因此當搜尋結束時需要使用`QUIT`回到正確的state
    * e.g 點選**點心與甜點**種類時，state轉換為`dessert_recipe`，並顯示pudding、chocolate、cookie、bread等細項，當選擇完後需要離開使state轉換為`search_recipe`就能繼續選擇其他**種類**的食譜繼續搜尋。
* 搜尋特定菜譜時，需要以`>> `作為前綴並輸入正確的值機器人才能順利搜尋

<p align="center">
	<img src="https://i.imgur.com/a8hn3xE.png"  width="500">
</p>

<p align="center">
	<img src="https://i.imgur.com/48p1exT.png"  width="500">
</p>

<p align="center">
	<img src="https://i.imgur.com/K3RufcF.png"  width="500">
</p>

<p align="center">
	<img src="https://i.imgur.com/egzogdl.png"  width="500">
</p>

<p align="center">
	<img src="https://i.imgur.com/s1hAXu4.jpg"  width="500">
</p>


### 幫助

在`idle`狀態的時候，可以輸入`help`查看幫助。此外，在任何狀態的時候，可以使用`information`來查看當前所在的state。

<p align="center">
	<img src="https://i.imgur.com/tJvOlRg.png"  width="500">
</p>

<p align="center">
	<img src="https://i.imgur.com/rfCdQmw.jpg"  width="500">
</p>


## 技術

* Render
<p align="center">
	<img src="https://i.imgur.com/ecblp0y.png"  width="900">
</p>

* Postgresql database
<p align="center">
	<img src="https://i.imgur.com/vYVvwuR.png"  width="900">
</p>

* Google Map API
<p align="center">
	<img src="https://i.imgur.com/WBG7hGK.png"  width="900">
</p>

* Web Crawling using bs4
<p align="center">
	<img src="https://i.imgur.com/oqxK8Zn.png"  width="900">
</p>


* Custom Flex Message
    

## FSM 圖

<p align="center">
	<img src="https://i.imgur.com/GsRHP8v.png"  width="900">
</p>


> -- :bust_in_silhouette: Dannyyang0329  :clock130: Sun, Dec 25, 2022 12:56 AM
