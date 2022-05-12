****An API for sheltered dog in spain****


**User API**

[GET] /user

       if current user = Admin, it pulls down all user databases 
       and sorts it in "public_id", "name", "password", "admin"
       
 [POST] /user

       if current user = Admin, creates new user with parimeters "name": {"psudoname", "password": int here}
       
 [GET] /user/<public_id>

       if current user = Admin, gets current specific user as "public_id", "name", "password", "admin"
       If none found, "No user found".
       
 [PUT] /user/<public_id>

       if current user = Admin, update current specific user with <public_id>
       If none found, "No user found" 
 
[DELETE] /user/<public_id>

       if current user = Admin, deletes the specified user.
       Returns "The user has been deleted" if it exists, otherwise "No user found"
       
 /login

       html request
 
 
 
 
 **Shelter Dogs API**

[POST] /dog/v1/create

       Creates a new dog with paremeters { "name": "Psudoname", "age": enter Int, "sex": "Female/Male",
       "breed": "Psudobreed", "color": "Psudocolor", "coat": "Psudocoat", "size": "Psudosize", 
       "neutered": "Yes/No", "likes_children": "Yes/No" }
       
       returns 501 if failed, otherwise "New dog created with the index:" with an unique index number
       
       
  [GET] /dog/v1/read/

       Loads all dogs in database and posts in the paremeters 'ID", "age", "breed", "name".
  
  [GET] /dog/v1/read/<name>

       Loads full data of all dogs with the name specified in url
  
       
 [PUT] /dog/v1/update

       updates a dog by searching for its ID and overwriting the rest of the data. 
       {"ID":2937,"name":"Adem","age":12,"sex":"Male","breed":"Shinu",
       "color":"orange","coat":"Short","size":"smol","neutered":"Yes","likes_children":"no"}
       Will overwrite everything but the ID. If you wish to keep the dog 
       the same and update just a small bit, copy the data from " [GET] /dog/v1/read/<name>" 
       and then change
       
 [DELETE] /dog/v1/<_id>

       Deletes the dog with the unique ID 
 
