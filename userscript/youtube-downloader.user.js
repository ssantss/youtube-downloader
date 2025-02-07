// ==UserScript==
// @name         YouTube Downloader Button
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  Agrega botón para descargar videos de YouTube
// @author       You
// @match        https://*.youtube.com/*
// @grant        GM_addStyle
// @run-at       document-idle
// ==/UserScript==

(function() {
    var tubeID = "dwnldBtn";
    var currentButton = "#owner";
    var addClick = `
        #${tubeID} {
            background-color: #F1F1F1;
            color: #191919;
            border: 1px solid;
            border-color: rgba(255,255,255,0.2);
            margin-left: 8px;
            padding: 0 16px;
            border-radius: 18px;
            font-size: 14px;
            font-family: Roboto, Noto, sans-serif;
            font-weight: 500;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            height: 36px;
            line-height: normal;
        }
        #${tubeID}:hover {
            background-color: #D9D9D9;
            color: #191919;
            border-color: #F1F1F1;
        }
    `;
    GM_addStyle(addClick);

    function openDownloader(url) {
        const downloaderUrl = `http://192.168.0.115:5270/?url=${encodeURIComponent(url)}`;
        const existingWindow = window.open(downloaderUrl, 'yt-downloader');
        
        if (existingWindow) {
            existingWindow.focus();
        }
    }

    function inspectPg(selector) {
        return new Promise(resolve => {
            if (document.querySelector(selector)) {
                return resolve(document.querySelector(selector));
            }
            var observer = new MutationObserver(mutations => {
                if (document.querySelector(selector)) {
                    resolve(document.querySelector(selector));
                    observer.disconnect();
                }
            });
            observer.observe(document.body,{childList: true, subtree: true});
        });
    }

    function addBtn() {
        inspectPg(currentButton).then((btnContainer) => {
            if (!btnContainer) return;

            if (!document.querySelector(`#${tubeID}`)) {
                var downloadBtn = document.createElement('a');
                downloadBtn.href = '#';
                downloadBtn.target = '_blank';
                downloadBtn.id = tubeID;
                downloadBtn.innerText = '🐧 DESCARGAR 🐧';
                downloadBtn.onclick = function(e) {
                    e.preventDefault();
                    openDownloader(window.location.href);
                };
                btnContainer.appendChild(downloadBtn);
            }
        });
    }

    let buttonSet = false;
    function checkButton() {
        if (window.location.pathname === '/watch' && !buttonSet) {
            addBtn();
            buttonSet = true;
        }
    }

    window.addEventListener("yt-navigate-finish", () => {
        buttonSet = false;
        checkButton();
    });

    checkButton();
})(); 