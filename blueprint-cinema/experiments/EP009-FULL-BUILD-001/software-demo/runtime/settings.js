'use strict';
const path=require('node:path');
module.exports={
 uiHost:'127.0.0.1',uiPort:1889,httpAdminRoot:'/red',httpNodeRoot:'/',
 userDir:path.join(__dirname,'.local','node-red'),flowFile:path.join(__dirname,'flows.json'),
 credentialSecret:process.env.EP009_NODE_RED_SECRET||false,
 editorTheme:{projects:{enabled:false},page:{title:'EP009 · Real Node-RED flow'}},
 functionGlobalContext:{ep009:require('./src/demo')},exportGlobalContextKeys:false,
 functionExternalModules:false,functionTimeout:10,
 logging:{console:{level:'warn',metrics:false,audit:false}},
 diagnostics:{enabled:false},runtimeState:{enabled:false},
 httpRequestTimeout:90000
};
