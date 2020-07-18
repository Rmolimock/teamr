/*!--------------------------------------------------------
 * Copyright (C) Microsoft Corporation. All rights reserved.
 *--------------------------------------------------------*/
(function(){var e=["vs/workbench/services/keybinding/browser/keyboardLayouts/_.contribution","require","exports","vs/workbench/services/keybinding/browser/keyboardLayouts/de.linux","vs/workbench/services/keybinding/browser/keyboardLayouts/en.linux","vs/workbench/services/keybinding/browser/keyboardLayouts/es.linux","vs/workbench/services/keybinding/browser/keyboardLayouts/fr.linux","vs/workbench/services/keybinding/browser/keyboardLayouts/ru.linux","vs/workbench/services/keybinding/browser/keyboardLayouts/layout.contribution.linux"],a=function(a){for(var t=[],r=0,o=a.length;r<o;r++)t[r]=e[a[r]];return t};define(e[0],a([1,2]),(function(e,a){"use strict";Object.defineProperty(a,"__esModule",{value:!0}),a.KeyboardLayoutContribution=void 0;let t=(()=>{class e{constructor(){this._layoutInfos=[]}get layoutInfos(){return this._layoutInfos}registerKeyboardLayout(e){this._layoutInfos.push(e)}}return e.INSTANCE=new e,e})();a.KeyboardLayoutContribution=t})),define(e[3],a([1,2,0]),(function(e,a,t){"use strict"
;Object.defineProperty(a,"__esModule",{value:!0}),t.KeyboardLayoutContribution.INSTANCE.registerKeyboardLayout({layout:{model:"pc104",layout:"de",variant:"",options:"",rules:"base"},secondaryLayouts:[],mapping:{Sleep:[],WakeUp:[],KeyA:["a","A","æ","Æ",0],KeyB:["b","B","“","‘",0],KeyC:["c","C","¢","©",0],KeyD:["d","D","ð","Ð",0],KeyE:["e","E","€","€",0],KeyF:["f","F","đ","ª",0],KeyG:["g","G","ŋ","Ŋ",0],KeyH:["h","H","ħ","Ħ",0],KeyI:["i","I","→","ı",0],KeyJ:["j","J","̣","̇",0],KeyK:["k","K","ĸ","&",0],KeyL:["l","L","ł","Ł",0],KeyM:["m","M","µ","º",0],KeyN:["n","N","”","’",0],KeyO:["o","O","ø","Ø",0],KeyP:["p","P","þ","Þ",0],KeyQ:["q","Q","@","Ω",0],KeyR:["r","R","¶","®",0],KeyS:["s","S","ſ","ẞ",0],KeyT:["t","T","ŧ","Ŧ",0],KeyU:["u","U","↓","↑",0],KeyV:["v","V","„","‚",0],KeyW:["w","W","ł","Ł",0],KeyX:["x","X","«","‹",0],KeyY:["z","Z","←","¥",0],KeyZ:["y","Y","»","›",0],Digit1:["1","!","¹","¡",0],Digit2:["2",'"',"²","⅛",0],Digit3:["3","§","³","£",0],Digit4:["4","$","¼","¤",0],Digit5:["5","%","½","⅜",0],
Digit6:["6","&","¬","⅝",0],Digit7:["7","/","{","⅞",0],Digit8:["8","(","[","™",0],Digit9:["9",")","]","±",0],Digit0:["0","=","}","°",0],Enter:["\r","\r","\r","\r",0],Escape:["","","","",0],Backspace:["\b","\b","\b","\b",0],Tab:["\t","","\t","",0],Space:[" "," "," "," ",0],Minus:["ß","?","\\","¿",0],Equal:["́","̀","̧","̨",0],BracketLeft:["ü","Ü","̈","̊",0],BracketRight:["+","*","~","¯",0],Backslash:["#","'","’","̆",0],Semicolon:["ö","Ö","̋","̣",0],Quote:["ä","Ä","̂","̌",0],Backquote:["̂","°","′","″",0],Comma:[",",";","·","×",0],Period:[".",":","…","÷",0],Slash:["-","_","–","—",0],CapsLock:[],F1:[],F2:[],F3:[],F4:[],F5:[],F6:[],F7:[],F8:[],F9:[],F10:[],F11:[],F12:[],PrintScreen:["","","","",0],ScrollLock:[],Pause:[],Insert:[],Home:[],PageUp:["/","/","/","/",0],Delete:[],End:[],PageDown:[],ArrowRight:[],ArrowLeft:[],ArrowDown:[],ArrowUp:[],NumLock:[],NumpadDivide:[],NumpadMultiply:["*","*","*","*",0],NumpadSubtract:["-","-","-","-",0],NumpadAdd:["+","+","+","+",0],NumpadEnter:[],Numpad1:["","1","","1",0],
Numpad2:["","2","","2",0],Numpad3:["","3","","3",0],Numpad4:["","4","","4",0],Numpad5:["","5","","5",0],Numpad6:["","6","","6",0],Numpad7:["","7","","7",0],Numpad8:["","8","","8",0],Numpad9:["","9","","9",0],Numpad0:["","0","","0",0],NumpadDecimal:["",",","",",",0],IntlBackslash:["<",">","|","̱",0],ContextMenu:[],Power:[],NumpadEqual:[],F13:[],F14:[],F15:[],F16:[],F17:[],F18:[],F19:[],F20:[],F21:[],F22:[],F23:[],F24:[],Open:[],Help:[],Select:[],Again:[],Undo:[],Cut:[],Copy:[],Paste:[],Find:[],AudioVolumeMute:[],AudioVolumeUp:[],AudioVolumeDown:[],NumpadComma:[],IntlRo:[],KanaMode:[],IntlYen:[],Convert:[],NonConvert:[],Lang1:[],Lang2:[],Lang3:[],Lang4:[],Lang5:[],NumpadParenLeft:[],NumpadParenRight:[],ControlLeft:[],ShiftLeft:[],AltLeft:[],MetaLeft:[],ControlRight:[],ShiftRight:[],AltRight:["\r","\r","\r","\r",0],MetaRight:[".",".",".",".",0],BrightnessUp:[],BrightnessDown:[],MediaPlay:[],MediaRecord:[],MediaFastForward:[],MediaRewind:[],MediaTrackNext:[],MediaTrackPrevious:[],MediaStop:[],Eject:[],
MediaPlayPause:[],MediaSelect:[],LaunchMail:[],LaunchApp2:[],LaunchApp1:[],SelectTask:[],LaunchScreenSaver:[],BrowserSearch:[],BrowserHome:[],BrowserBack:[],BrowserForward:[],BrowserStop:[],BrowserRefresh:[],BrowserFavorites:[],MailReply:[],MailForward:[],MailSend:[]}})})),define(e[4],a([1,2,0]),(function(e,a,t){"use strict";Object.defineProperty(a,"__esModule",{value:!0}),t.KeyboardLayoutContribution.INSTANCE.registerKeyboardLayout({layout:{model:"pc105",layout:"us",variant:"",options:"",rules:"evdev",isUSStandard:!0},secondaryLayouts:[{model:"pc105",layout:"cn",variant:"",options:"",rules:"evdev"}],mapping:{Sleep:[],WakeUp:[],KeyA:["a","A","a","A",0],KeyB:["b","B","b","B",0],KeyC:["c","C","c","C",0],KeyD:["d","D","d","D",0],KeyE:["e","E","e","E",0],KeyF:["f","F","f","F",0],KeyG:["g","G","g","G",0],KeyH:["h","H","h","H",0],KeyI:["i","I","i","I",0],KeyJ:["j","J","j","J",0],KeyK:["k","K","k","K",0],KeyL:["l","L","l","L",0],KeyM:["m","M","m","M",0],KeyN:["n","N","n","N",0],KeyO:["o","O","o","O",0],
KeyP:["p","P","p","P",0],KeyQ:["q","Q","q","Q",0],KeyR:["r","R","r","R",0],KeyS:["s","S","s","S",0],KeyT:["t","T","t","T",0],KeyU:["u","U","u","U",0],KeyV:["v","V","v","V",0],KeyW:["w","W","w","W",0],KeyX:["x","X","x","X",0],KeyY:["y","Y","y","Y",0],KeyZ:["z","Z","z","Z",0],Digit1:["1","!","1","!",0],Digit2:["2","@","2","@",0],Digit3:["3","#","3","#",0],Digit4:["4","$","4","$",0],Digit5:["5","%","5","%",0],Digit6:["6","^","6","^",0],Digit7:["7","&","7","&",0],Digit8:["8","*","8","*",0],Digit9:["9","(","9","(",0],Digit0:["0",")","0",")",0],Enter:["\r","\r","\r","\r",0],Escape:["","","","",0],Backspace:["\b","\b","\b","\b",0],Tab:["\t","","\t","",0],Space:[" "," "," "," ",0],Minus:["-","_","-","_",0],Equal:["=","+","=","+",0],BracketLeft:["[","{","[","{",0],BracketRight:["]","}","]","}",0],Backslash:["\\","|","\\","|",0],Semicolon:[";",":",";",":",0],Quote:["'",'"',"'",'"',0],Backquote:["`","~","`","~",0],Comma:[",","<",",","<",0],Period:[".",">",".",">",0],Slash:["/","?","/","?",0],CapsLock:[],F1:[],F2:[],
F3:[],F4:[],F5:[],F6:[],F7:[],F8:[],F9:[],F10:[],F11:[],F12:[],PrintScreen:[],ScrollLock:[],Pause:[],Insert:[],Home:[],PageUp:[],Delete:["","","","",0],End:[],PageDown:[],ArrowRight:[],ArrowLeft:[],ArrowDown:[],ArrowUp:[],NumLock:[],NumpadDivide:["/","/","/","/",0],NumpadMultiply:["*","*","*","*",0],NumpadSubtract:["-","-","-","-",0],NumpadAdd:["+","+","+","+",0],NumpadEnter:["\r","\r","\r","\r",0],Numpad1:["","1","","1",0],Numpad2:["","2","","2",0],Numpad3:["","3","","3",0],Numpad4:["","4","","4",0],Numpad5:["","5","","5",0],Numpad6:["","6","","6",0],Numpad7:["","7","","7",0],Numpad8:["","8","","8",0],Numpad9:["","9","","9",0],Numpad0:["","0","","0",0],NumpadDecimal:["",".","",".",0],IntlBackslash:["<",">","|","¦",0],ContextMenu:[],Power:[],NumpadEqual:["=","=","=","=",0],F13:[],F14:[],F15:[],F16:[],F17:[],F18:[],F19:[],F20:[],F21:[],F22:[],F23:[],F24:[],Open:[],Help:[],Select:[],Again:[],Undo:[],Cut:[],Copy:[],Paste:[],Find:[],AudioVolumeMute:[],AudioVolumeUp:[],AudioVolumeDown:[],
NumpadComma:[".",".",".",".",0],IntlRo:[],KanaMode:[],IntlYen:[],Convert:[],NonConvert:[],Lang1:[],Lang2:[],Lang3:[],Lang4:[],Lang5:[],NumpadParenLeft:["(","(","(","(",0],NumpadParenRight:[")",")",")",")",0],ControlLeft:[],ShiftLeft:[],AltLeft:[],MetaLeft:[],ControlRight:[],ShiftRight:[],AltRight:[],MetaRight:[],BrightnessUp:[],BrightnessDown:[],MediaPlay:[],MediaRecord:[],MediaFastForward:[],MediaRewind:[],MediaTrackNext:[],MediaTrackPrevious:[],MediaStop:[],Eject:[],MediaPlayPause:[],MediaSelect:[],LaunchMail:[],LaunchApp2:[],LaunchApp1:[],SelectTask:[],LaunchScreenSaver:[],BrowserSearch:[],BrowserHome:[],BrowserBack:[],BrowserForward:[],BrowserStop:[],BrowserRefresh:[],BrowserFavorites:[],MailReply:[],MailForward:[],MailSend:[]}})})),define(e[5],a([1,2,0]),(function(e,a,t){"use strict";Object.defineProperty(a,"__esModule",{value:!0}),t.KeyboardLayoutContribution.INSTANCE.registerKeyboardLayout({layout:{model:"pc105",layout:"es",variant:"",options:"",rules:"evdev"},secondaryLayouts:[],mapping:{Sleep:[],
WakeUp:[],KeyA:["a","A","æ","Æ",0],KeyB:["b","B","”","’",0],KeyC:["c","C","¢","©",0],KeyD:["d","D","ð","Ð",0],KeyE:["e","E","€","¢",0],KeyF:["f","F","đ","ª",0],KeyG:["g","G","ŋ","Ŋ",0],KeyH:["h","H","ħ","Ħ",0],KeyI:["i","I","→","ı",0],KeyJ:["j","J","̉","̛",0],KeyK:["k","K","ĸ","&",0],KeyL:["l","L","ł","Ł",0],KeyM:["m","M","µ","º",0],KeyN:["n","N","n","N",0],KeyO:["o","O","ø","Ø",0],KeyP:["p","P","þ","Þ",0],KeyQ:["q","Q","@","Ω",0],KeyR:["r","R","¶","®",0],KeyS:["s","S","ß","§",0],KeyT:["t","T","ŧ","Ŧ",0],KeyU:["u","U","↓","↑",0],KeyV:["v","V","“","‘",0],KeyW:["w","W","ł","Ł",0],KeyX:["x","X","»",">",0],KeyY:["y","Y","←","¥",0],KeyZ:["z","Z","«","<",0],Digit1:["1","!","|","¡",0],Digit2:["2",'"',"@","⅛",0],Digit3:["3","·","#","£",0],Digit4:["4","$","~","$",0],Digit5:["5","%","½","⅜",0],Digit6:["6","&","¬","⅝",0],Digit7:["7","/","{","⅞",0],Digit8:["8","(","[","™",0],Digit9:["9",")","]","±",0],Digit0:["0","=","}","°",0],Enter:["\r","\r","\r","\r",0],Escape:["","","","",0],Backspace:["\b","\b","\b","\b",0],
Tab:["\t","","\t","",0],Space:[" "," "," "," ",0],Minus:["'","?","\\","¿",0],Equal:["¡","¿","̃","~",0],BracketLeft:["̀","̂","[","̊",0],BracketRight:["+","*","]","̄",0],Backslash:["ç","Ç","}","̆",0],Semicolon:["ñ","Ñ","~","̋",0],Quote:["́","̈","{","{",0],Backquote:["º","ª","\\","\\",0],Comma:[",",";","─","×",0],Period:[".",":","·","÷",0],Slash:["-","_","̣","̇",0],CapsLock:[],F1:[],F2:[],F3:[],F4:[],F5:[],F6:[],F7:[],F8:[],F9:[],F10:[],F11:[],F12:[],PrintScreen:[],ScrollLock:[],Pause:[],Insert:[],Home:[],PageUp:[],Delete:["","","","",0],End:[],PageDown:[],ArrowRight:[],ArrowLeft:[],ArrowDown:[],ArrowUp:[],NumLock:[],NumpadDivide:["/","/","/","/",0],NumpadMultiply:["*","*","*","*",0],NumpadSubtract:["-","-","-","-",0],NumpadAdd:["+","+","+","+",0],NumpadEnter:["\r","\r","\r","\r",0],Numpad1:["","1","","1",0],Numpad2:["","2","","2",0],Numpad3:["","3","","3",0],Numpad4:["","4","","4",0],Numpad5:["","5","","5",0],Numpad6:["","6","","6",0],Numpad7:["","7","","7",0],Numpad8:["","8","","8",0],
Numpad9:["","9","","9",0],Numpad0:["","0","","0",0],NumpadDecimal:["",".","",".",0],IntlBackslash:["<",">","|","¦",0],ContextMenu:[],Power:[],NumpadEqual:["=","=","=","=",0],F13:[],F14:[],F15:[],F16:[],F17:[],F18:[],F19:[],F20:[],F21:[],F22:[],F23:[],F24:[],Open:[],Help:[],Select:[],Again:[],Undo:[],Cut:[],Copy:[],Paste:[],Find:[],AudioVolumeMute:[],AudioVolumeUp:[],AudioVolumeDown:[],NumpadComma:[".",".",".",".",0],IntlRo:[],KanaMode:[],IntlYen:[],Convert:[],NonConvert:[],Lang1:[],Lang2:[],Lang3:[],Lang4:[],Lang5:[],NumpadParenLeft:["(","(","(","(",0],NumpadParenRight:[")",")",")",")",0],ControlLeft:[],ShiftLeft:[],AltLeft:[],MetaLeft:[],ControlRight:[],ShiftRight:[],AltRight:[],MetaRight:[],BrightnessUp:[],BrightnessDown:[],MediaPlay:[],MediaRecord:[],MediaFastForward:[],MediaRewind:[],MediaTrackNext:[],MediaTrackPrevious:[],MediaStop:[],Eject:[],MediaPlayPause:[],MediaSelect:[],LaunchMail:[],LaunchApp2:[],LaunchApp1:[],SelectTask:[],LaunchScreenSaver:[],BrowserSearch:[],BrowserHome:[],BrowserBack:[],
BrowserForward:[],BrowserStop:[],BrowserRefresh:[],BrowserFavorites:[],MailReply:[],MailForward:[],MailSend:[]}})})),define(e[6],a([1,2,0]),(function(e,a,t){"use strict";Object.defineProperty(a,"__esModule",{value:!0}),t.KeyboardLayoutContribution.INSTANCE.registerKeyboardLayout({layout:{model:"pc104",layout:"fr",variant:"",options:"",rules:"base"},secondaryLayouts:[],mapping:{Sleep:[],WakeUp:[],KeyA:["q","Q","@","Ω",0],KeyB:["b","B","”","’",0],KeyC:["c","C","¢","©",0],KeyD:["d","D","ð","Ð",0],KeyE:["e","E","€","¢",0],KeyF:["f","F","đ","ª",0],KeyG:["g","G","ŋ","Ŋ",0],KeyH:["h","H","ħ","Ħ",0],KeyI:["i","I","→","ı",0],KeyJ:["j","J","̉","̛",0],KeyK:["k","K","ĸ","&",0],KeyL:["l","L","ł","Ł",0],KeyM:[",","?","́","̋",0],KeyN:["n","N","n","N",0],KeyO:["o","O","ø","Ø",0],KeyP:["p","P","þ","Þ",0],KeyQ:["a","A","æ","Æ",0],KeyR:["r","R","¶","®",0],KeyS:["s","S","ß","§",0],KeyT:["t","T","ŧ","Ŧ",0],KeyU:["u","U","↓","↑",0],KeyV:["v","V","“","‘",0],KeyW:["z","Z","«","<",0],KeyX:["x","X","»",">",0],KeyY:["y","Y","←","¥",0],
KeyZ:["w","W","ł","Ł",0],Digit1:["&","1","¹","¡",0],Digit2:["é","2","~","⅛",0],Digit3:['"',"3","#","£",0],Digit4:["'","4","{","$",0],Digit5:["(","5","[","⅜",0],Digit6:["-","6","|","⅝",0],Digit7:["è","7","`","⅞",0],Digit8:["_","8","\\","™",0],Digit9:["ç","9","^","±",0],Digit0:["à","0","@","°",0],Enter:["\r","\r","\r","\r",0],Escape:["","","","",0],Backspace:["\b","\b","\b","\b",0],Tab:["\t","","\t","",0],Space:[" "," "," "," ",0],Minus:[")","°","]","¿",0],Equal:["=","+","}","̨",0],BracketLeft:["̂","̈","̈","̊",0],BracketRight:["$","£","¤","̄",0],Backslash:["*","µ","̀","̆",0],Semicolon:["m","M","µ","º",0],Quote:["ù","%","̂","̌",0],Backquote:["²","~","¬","¬",0],Comma:[";",".","─","×",0],Period:[":","/","·","÷",0],Slash:["!","§","̣","̇",0],CapsLock:[],F1:[],F2:[],F3:[],F4:[],F5:[],F6:[],F7:[],F8:[],F9:[],F10:[],F11:[],F12:[],PrintScreen:["","","","",0],ScrollLock:[],Pause:[],Insert:[],Home:[],PageUp:["/","/","/","/",0],Delete:[],End:[],PageDown:[],ArrowRight:[],ArrowLeft:[],ArrowDown:[],ArrowUp:[],NumLock:[],
NumpadDivide:[],NumpadMultiply:["*","*","*","*",0],NumpadSubtract:["-","-","-","-",0],NumpadAdd:["+","+","+","+",0],NumpadEnter:[],Numpad1:["","1","","1",0],Numpad2:["","2","","2",0],Numpad3:["","3","","3",0],Numpad4:["","4","","4",0],Numpad5:["","5","","5",0],Numpad6:["","6","","6",0],Numpad7:["","7","","7",0],Numpad8:["","8","","8",0],Numpad9:["","9","","9",0],Numpad0:["","0","","0",0],NumpadDecimal:["",".","",".",0],IntlBackslash:["<",">","|","¦",0],ContextMenu:[],Power:[],NumpadEqual:[],F13:[],F14:[],F15:[],F16:[],F17:[],F18:[],F19:[],F20:[],F21:[],F22:[],F23:[],F24:[],Open:[],Help:[],Select:[],Again:[],Undo:[],Cut:[],Copy:[],Paste:[],Find:[],AudioVolumeMute:[],AudioVolumeUp:[],AudioVolumeDown:[],NumpadComma:[],IntlRo:[],KanaMode:[],IntlYen:[],Convert:[],NonConvert:[],Lang1:[],Lang2:[],Lang3:[],Lang4:[],Lang5:[],NumpadParenLeft:[],NumpadParenRight:[],ControlLeft:[],ShiftLeft:[],AltLeft:[],MetaLeft:[],ControlRight:[],ShiftRight:[],AltRight:["\r","\r","\r","\r",0],MetaRight:[".",".",".",".",0],
BrightnessUp:[],BrightnessDown:[],MediaPlay:[],MediaRecord:[],MediaFastForward:[],MediaRewind:[],MediaTrackNext:[],MediaTrackPrevious:[],MediaStop:[],Eject:[],MediaPlayPause:[],MediaSelect:[],LaunchMail:[],LaunchApp2:[],LaunchApp1:[],SelectTask:[],LaunchScreenSaver:[],BrowserSearch:[],BrowserHome:[],BrowserBack:[],BrowserForward:[],BrowserStop:[],BrowserRefresh:[],BrowserFavorites:[],MailReply:[],MailForward:[],MailSend:[]}})})),define(e[7],a([1,2,0]),(function(e,a,t){"use strict";Object.defineProperty(a,"__esModule",{value:!0}),t.KeyboardLayoutContribution.INSTANCE.registerKeyboardLayout({layout:{model:"pc104",layout:"ru",variant:",",options:"",rules:"base"},secondaryLayouts:[],mapping:{Sleep:[],WakeUp:[],KeyA:["ф","Ф","ф","Ф",0],KeyB:["и","И","и","И",0],KeyC:["с","С","с","С",0],KeyD:["в","В","в","В",0],KeyE:["у","У","у","У",0],KeyF:["а","А","а","А",0],KeyG:["п","П","п","П",0],KeyH:["р","Р","р","Р",0],KeyI:["ш","Ш","ш","Ш",0],KeyJ:["о","О","о","О",0],KeyK:["л","Л","л","Л",0],KeyL:["д","Д","д","Д",0],
KeyM:["ь","Ь","ь","Ь",0],KeyN:["т","Т","т","Т",0],KeyO:["щ","Щ","щ","Щ",0],KeyP:["з","З","з","З",0],KeyQ:["й","Й","й","Й",0],KeyR:["к","К","к","К",0],KeyS:["ы","Ы","ы","Ы",0],KeyT:["е","Е","е","Е",0],KeyU:["г","Г","г","Г",0],KeyV:["м","М","м","М",0],KeyW:["ц","Ц","ц","Ц",0],KeyX:["ч","Ч","ч","Ч",0],KeyY:["н","Н","н","Н",0],KeyZ:["я","Я","я","Я",0],Digit1:["1","!","1","!",0],Digit2:["2",'"',"2",'"',0],Digit3:["3","№","3","№",0],Digit4:["4",";","4",";",0],Digit5:["5","%","5","%",0],Digit6:["6",":","6",":",0],Digit7:["7","?","7","?",0],Digit8:["8","*","₽","",0],Digit9:["9","(","9","(",0],Digit0:["0",")","0",")",0],Enter:["\r","\r","\r","\r",0],Escape:["","","","",0],Backspace:["\b","\b","\b","\b",0],Tab:["\t","","\t","",0],Space:[" "," "," "," ",0],Minus:["-","_","-","_",0],Equal:["=","+","=","+",0],BracketLeft:["х","Х","х","Х",0],BracketRight:["ъ","Ъ","ъ","Ъ",0],Backslash:["\\","/","\\","/",0],Semicolon:["ж","Ж","ж","Ж",0],Quote:["э","Э","э","Э",0],Backquote:["ё","Ё","ё","Ё",0],Comma:["б","Б","б","Б",0],
Period:["ю","Ю","ю","Ю",0],Slash:[".",",",".",",",0],CapsLock:[],F1:[],F2:[],F3:[],F4:[],F5:[],F6:[],F7:[],F8:[],F9:[],F10:[],F11:[],F12:[],PrintScreen:["","","","",0],ScrollLock:[],Pause:[],Insert:[],Home:[],PageUp:["/","/","/","/",0],Delete:[],End:[],PageDown:[],ArrowRight:[],ArrowLeft:[],ArrowDown:[],ArrowUp:[],NumLock:[],NumpadDivide:[],NumpadMultiply:["*","*","*","*",0],NumpadSubtract:["-","-","-","-",0],NumpadAdd:["+","+","+","+",0],NumpadEnter:[],Numpad1:["","1","","1",0],Numpad2:["","2","","2",0],Numpad3:["","3","","3",0],Numpad4:["","4","","4",0],Numpad5:["","5","","5",0],Numpad6:["","6","","6",0],Numpad7:["","7","","7",0],Numpad8:["","8","","8",0],Numpad9:["","9","","9",0],Numpad0:["","0","","0",0],NumpadDecimal:["",",","",",",0],IntlBackslash:["/","|","|","¦",0],ContextMenu:[],Power:[],NumpadEqual:[],F13:[],F14:[],F15:[],F16:[],F17:[],F18:[],F19:[],F20:[],F21:[],F22:[],F23:[],F24:[],Open:[],Help:[],Select:[],Again:[],Undo:[],Cut:[],Copy:[],Paste:[],Find:[],AudioVolumeMute:[],AudioVolumeUp:[],
AudioVolumeDown:[],NumpadComma:[],IntlRo:[],KanaMode:[],IntlYen:[],Convert:[],NonConvert:[],Lang1:[],Lang2:[],Lang3:[],Lang4:[],Lang5:[],NumpadParenLeft:[],NumpadParenRight:[],ControlLeft:[],ShiftLeft:[],AltLeft:[],MetaLeft:[],ControlRight:[],ShiftRight:[],AltRight:["\r","\r","\r","\r",0],MetaRight:[".",".",".",".",0],BrightnessUp:[],BrightnessDown:[],MediaPlay:[],MediaRecord:[],MediaFastForward:[],MediaRewind:[],MediaTrackNext:[],MediaTrackPrevious:[],MediaStop:[],Eject:[],MediaPlayPause:[],MediaSelect:[],LaunchMail:[],LaunchApp2:[],LaunchApp1:[],SelectTask:[],LaunchScreenSaver:[],BrowserSearch:[],BrowserHome:[],BrowserBack:[],BrowserForward:[],BrowserStop:[],BrowserRefresh:[],BrowserFavorites:[],MailReply:[],MailForward:[],MailSend:[]}})})),define(e[8],a([1,2,0,4,5,3,6,7]),(function(e,a,t){"use strict";Object.defineProperty(a,"__esModule",{value:!0}),Object.defineProperty(a,"KeyboardLayoutContribution",{enumerable:!0,get:function(){return t.KeyboardLayoutContribution}})}))}).call(this);
//# sourceMappingURL=layout.contribution.linux.js.map
