
import * as React from 'react';
import { Socket } from './Socket';
import TwitterLogin from 'react-twitter-auth/lib/react-twitter-auth-component.js';
import './css/button.css';

export function TestButton() 
{
    // const [success, setSuccess] = React.useState(false);
    // const [failed, setFailed] = React.useState(false);

    function onSuccess(response) {
        response.json().then(body => {
            alert(JSON.stringify(body));
        });
      }
    
      function onFailed(error) {
          alert(error);
      }

        return (
          <div>
            <TwitterLogin loginUrl="http://vm:8080/api/v1/auth/twitter"
                          onFailure={this.onFailed}
                          onSuccess={this.onSuccess}
                          requestTokenUrl="http://vm:8080/api/v1/auth/twitter/reverse"
                          showIcon={true}
                          forceLogin={true}/>
    
            <TwitterLogin loginUrl="http://vm:8080/api/v1/auth/twitter"
                          onFailure={this.onFailed}
                          onSuccess={this.onSuccess}
                          requestTokenUrl="http://vm:8080/api/v1/auth/twitter/reverse"
                          showIcon={true}>
              <b>Custom</b> Twitter <i>Login</i> content
            </TwitterLogin>
          </div>
        );
}