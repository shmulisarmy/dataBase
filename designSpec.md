# Execution cycle


Before running this, any basic single {creates, selects, updates} will run assuming the're only dealing with one row and are going to be really quick 

I’m taking the approach of first collecting the rows and then updating them for separation of concerns that way when multi threading I don’t have to block (mutex lock) as much


There will be switch between only selects and row gathering for non table joining update queries wich can happen all at the same time because their all a mutex acces of type view 

Once that’s done the non join (minimal change affected and affecting) rows will go through their to update lists and and update appropriately 





## Get newest flag 

Although the rows in this round are not interlocked/depent on other rows (and there by won’t be affected by other rows getting updated (both in their table and in any other)) if the user has the “Get newest” flag on then extra work will be put in to make sure they have the newest data they can get





# Execution plan 




## non Table Join and non Graph linked update queries


while first checking each one in a set if thev'e changed to wich they will be revalidated 

And after wards they will revalidate ones they missed that were updated in that round


Rows with the “get newest” flag will run after regular rows in order of the amount of rows that they need to update (as is known before running the revalidation)




## table join update queries

these will run one at a time 





# Query planning



There are many different ways to validate a row for selection or updating and depending on how you plan to validate will your rows will affect the Query planning process


Cell validation types


### == 

Can only validate one at a time  (can’t validate based order, is exact)


### => 

•⁠  ⁠[ ] Comes back with many results 
•⁠  ⁠[ ] Automatic ordering 
•⁠  ⁠[ ] Can validate many rows at the same time (if in index map)


### SearchTree[“he”] -> [“help”, “hello”]

Can collect many at a time (if is first part of the query plan)

Limits down to a few options


### SearchTree[“he”, excusable=1]-> [“hello”, “help”, “hi”]

Can collect many at a time (if is first part of the query plan)

Can come back with many results


As you can see here it really makes a difference wich order we validate in 

Our best preference is that there is field that needs to be validated that is stored In a map to wich if we multiple we will choose the one with the shortest length (less to go through when validating the rest of the fields)

Our second preference is the search tree 
With out execusables


Then == because we still need to check by at least limit the results


Rollbacks

In case of emergency shut down


Single updates 

When one update is executing at a time the way rollbacks are going to work is after gathering the list of row ids they will be stored on disc and if there’s a shutdown
