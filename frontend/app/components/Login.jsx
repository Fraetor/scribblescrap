"use client"

import React from 'react';
import Cookies from 'js-cookie';
import { useEffect, useState } from "react";
import { useGetCookie } from './getCookie';


export default function Login () {
    const [isOpen, setIsOpen] = useState(false);
    const [username, setUsername] = useState('');
    const [typing, setTyping] = useState('');

    const cookie = useGetCookie('username');

    useEffect(() => {
        console.log(cookie)
        if (cookie) {
            setUsername(cookie);
        }
    }, [cookie]);

    const openModal = () => {
      setIsOpen(true);
    };

    const closeModal = () => {
      setIsOpen(false);
    };

    const handleInputChange = (e) => {
        setTyping(e.target.value);
    };

    const postLogin = async () => {
        setUsername(typing)
        try {
          const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "username": typing })
          });
      
          if (!response.ok) {
            // Handle error response, e.g., show error message to user
            throw new Error('Login failed');
          }
      
          // Assuming the server responds with JSON data
          const data = await response.json();
      
          // Handle successful login response, e.g., update state or perform navigation
          console.log('Login successful', data);
        } catch (error) {
          // Handle fetch errors, e.g., network errors
          console.error('Login error:', error.message);
        }
        closeModal()
      };

    return (
      <div>
        {(username !== "") && (
            <span className="pr-4">Welcome, {username}</span>
        )}
        <button
          className="bg-orange-600 text-white p-2 rounded"
          onClick={openModal}
        >
          Login
        </button>

        {isOpen && (
          <div className="fixed inset-0 flex items-center justify-center z-50">
            <div className="modal-overlay fixed inset-0 bg-black opacity-50" />
            <div className="modal-container w-11/12 md:max-w-md mx-auto z-50 overflow-y-auto">
              <div className="modal-content py-4 text-left px-6 shadow-lg">
                <div className="flex bg-green-700 justify-between items-center  p-3 rounded-t-lg">
                  <p className="text-2xl text-yellow-500 font-bold">Login</p>
                  <button
                    className="modal-close p-2 -mt-2 -mr-2 rounded-full hover:bg-green-800"
                    onClick={closeModal}
                  >
                    <svg
                      className="w-6 h-6 text-yellow-500"
                      role="button"
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 18 18"
                    >
                      <path
                        fill="currentColor"
                        d="M12.727,6 L9,9.727 L5.273,6 L4.586,6.686 L8.313,10.414 L4.586,14.141 L5.273,14.828 L9,11.101 L12.727,14.828 L13.414,14.141 L9.687,10.414 L13.414,6.686 L12.727,6 Z"
                      ></path>
                    </svg>
                  </button>
                </div>
                <div className="border-4 bg-yellow-100 rounded-b-lg border-green-700 border-t-0 text-black text-lg p-4">
                  <p>Enter Username</p>
                  <input
                    type="text"
                    value={typing}
                    onChange={handleInputChange}
                    className="border border-gray-400 p-2 mb-4 w-full"
                  />
                  <button
                    onClick={() => postLogin(username)}
                    className="bg-orange-600 text-white p-2 rounded"
                  >
                    Set Username
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    );
}