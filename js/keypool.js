/* Returns a function to generate unique keys from a pool.
   
   Example:
   
     var pool = keyPool();        
     pool.newKey();                   // returns 0, which is allocated immedately
     pool.newKey();                   // returns 1
     pool.delKey(0);                  // deletes 0
     pool.set('some value');          // assigns a value and returns its key                                    
     pool.get(0);                     // gets the value with key 0
*/
var keyPool = function() {
  var data = {};
  var free = [[0, Infinity]];       // Contains ranges of free ids
  
  // Is a key taken?
  var is_taken = function(i, key) {
     return (i == 0) ? key < free[i][0] 
                     : key > free[i-1][1] && key < free[i][0];
  };       
  
  var merge_and_add = function(i, key) {
    free.splice(i, 0, [key, key]);
    if (i < free.length - 1 && free[i+1][0] === free[i][1] + 1) {
        free[i+1][0] = free[i][0];
        free.splice(i, 1);
    }
    if (i > 0 && free[i-1][1] === free[i][0] - 1) {
        free[i-1][1] = free[i][1]
        free.splice(i, 1);
    }
    delete data[key];
  };

  var newKey = function() {
     var ret = free[0][0];
     (free[0][0] === free[0][1]) ? free.splice(0, 1) : free[0][0] += 1;
     return ret;
  };

  return {
     'set' : function() {
        if (arguments.length == 1) {
           var key = newKey();
           data[key] = arguments[0];
           return key;
        }
        else if (arguments.length == 2) {
           data[arguments[0]] = arguments[1];
           return arguments[0];
        }
        else {
           throw new ValueError();
        }
     },
     'get' : function(key) {
        return data[parseInt(key)];
     },
     'newKey' : function() {
        return newKey();
     },    
     'delKey' : function(key) {
        key = parseInt(key);
        if (key < 0 || key > Infinity)
           throw new ValueError();

        var p = Math.floor(Math.random() * free.length);
        var d = 0;
        var max_d = Math.log(free.length) + 1;
          
        while (d <= max_d) {
           if (is_taken(p, key))      
              return merge_and_add(p, key);
           else if (key < free[p][0]) 
              p = Math.floor(p/2);            
           else if (key > free[p][1])
              p += Math.floor((free.length - p)/2);            
           d += 1;
        }                  
     }
  }
}