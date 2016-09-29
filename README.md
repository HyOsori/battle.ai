# back_end

set ".gitignore" file
it ignores 'Pycharm', 'Virtualenv', 'tornado'


```
Web page                     Back end                     AI Client
   |                             |                             |
   |                             |                             |
   | ---- Request User List ---> |                             |
   | <--- Response User List --- |                             |
   |                             |                             |
   |                             |                             |
   |                             | <-------- Connect --------- |
   | <--- Notice User Added ---- |                             |
   |                             |                             |
   |                             |                             |
   |                             | <------- Disconnect ------- |
   | <-- Notice User Removed --- |                             |
   |                             |                             |
   |                             |                             |
   | ------ Request Match -----> |                             |
   |                             | --- Request Game Start ---> |
   |                             | <-- Response Game Start --- |
   | <----- Response Match ----- |                             |
   |                             |                             |
   |                             |                             |
   |                             | --- Request Game Data ----> |
   |                             |                             |
   |                             | <-- Response Game Data ---- |
   |                             |                             |
   | <----- Send Game Data ----- |                             |
   |                             |                             |
   |             '''             |                             |
   |                             |                             |
```

```
 AI client                     Server                      GameLogic
   |                             |                             |
   |                             |                             |
   | --------- Connect --------> |                             |
   |                             |                             |
   | ----- Send User Info -----> |                             |
   | <---- Check id is valid --- |                             |
   |


            ============================================
   |                             |                             |
   | <--- Are You Ready ??? ---- |                             |
   | --------- OK -------------> |                             |
   |                             |                             |
   |                             | ---------- OnStart  ------> |
   |                             |                             |
   |                             | <--- Request Game Data ---- |
   | <-- Request Game Data ----- |                             |
   |                             |                             |
   |                             |                             |
   | -- Response Game Data  ---> |                             |
   |                             | -------- OnAction --------> |
   |                             |                             |
   |                             | <--- Request Game Data ---- |
   | <-- Request Game Data ----- |                             |
   |                             |                             |
   |                             |                             |
   | -- Response Game Data  ---> |                             |
   |                             | -------- OnAction --------> |
                     .........................

   |                             |  <--------- finish--------- |
   | <-------- finish ---------- |                             |
   | ------- OK ---------------> |                             |
   |                             | ------------ OK ----------> |
   |                             | <------- round result ------|
   | <----- round result ------- |                             |
            ===============================================


   | <------ game result ------- |                             |
```