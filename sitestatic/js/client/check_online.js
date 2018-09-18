/**
 * Created by munis on 7/18/17.
 */
//Client-side parent variable declaration (simulated namespacing)
        var Client = Client || {};
        Client.Pulse = null; //Holds a pointer to the heartbeat timer (id)
        /* If you needed to cancel the heartbeat processes you could
         * pass this variable to clearTimeout(). Calling Client.Heartbeat()
         * again would start the cycle back up.
         */

        //Initial event that will kick off the chain when the DOM is ready
        $(document).ready(function(){
          Client.Heartbeat(); //Initial call to the Heartbeat function
        });//ready

        /// Sends the heartbeat signal and retrieves the currently active user list
        Client.Heartbeat = function(){
          var sUsername = 'SomeUser';
          /* Note: If you have an active session running on the server it would not be
           * necessary to send the username since you could pull it on the backend
           * script which would be more tamper-proof anyway. I'm just giving an
           * example of sending data to the server using the jQuery.ajax method
           * If you were storing the username to be sent from the client; this wouldn't
           * be a good place to do it anyway
           *
           * Remove the "data : {...}" line below to exclude sending information to the server
           * The "type : 'post'" line would not be necessary either
           */

          $.ajax({ //Send the signal and recieve the information about active users back
                url : '/check/online/',
                type : 'post',
                dataType : 'json',
                data : {Username : sUsername },
                success : function(jActiveUsers,sStatus,jqXHR){
                  /* This is the callback function of the request, jActiveUsers will be the
                   * json object with the information you choose to send back to it
                   */
                  Client.RenderActiveUsers(jActiveUsers); //Call the display function
                  //Trigger the next delayed call to Client.Heartbeat
                  Client.Pulse = setTimeout(function(){
                    Client.Heartbeat();
                  },3000); //3 second delay before next trigger
                }//success
              });//$.ajax
            }//Heartbeat

        /// Processes the results sent by the server and draws them to the UI
        Client.RenderActiveUsers = function(jActiveUsers){
          console.log(jActiveUsers);
        }//RenderActiveUsers