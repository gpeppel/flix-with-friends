
import * as React from 'react';
// import './css/header.css';

export function Header() 
{
        return (
            <div style={{
                display: 'flex',
                flexDirection: 'column',
                height: '100%'
            }}>
            <div className='main-header'>
                <img className='logo' src="static/images/logo.png" alt="logo" />
            </div>
            </div>
        );
}
