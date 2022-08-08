/* global toastr */

/**
 * --------------------------------------------------------------------------
 * CoreUI Pro Boostrap Admin Template (2.0.1): toastr.js
 * Licensed under MIT (https://coreui.io/license)
 * --------------------------------------------------------------------------
 */

/*
 * Note that this is toastr v2.1.3, the "latest" version in url has no more maintenance,
 * please go to https://cdnjs.com/libraries/toastr.js and pick a certain version you want to use,
 * make sure you copy the url from the website since the url may change between versions.
 * */
!function(e){e(["jquery"],function(e){return function(){function t(e,t,n){return g({type:O.error,iconClass:m().iconClasses.error,message:e,optionsOverride:n,title:t})}function n(t,n){return t||(t=m()),v=e("#"+t.containerId),v.length?v:(n&&(v=d(t)),v)}function o(e,t,n){return g({type:O.info,iconClass:m().iconClasses.info,message:e,optionsOverride:n,title:t})}function s(e){C=e}function i(e,t,n){return g({type:O.success,iconClass:m().iconClasses.success,message:e,optionsOverride:n,title:t})}function a(e,t,n){return g({type:O.warning,iconClass:m().iconClasses.warning,message:e,optionsOverride:n,title:t})}function r(e,t){var o=m();v||n(o),u(e,o,t)||l(o)}function c(t){var o=m();return v||n(o),t&&0===e(":focus",t).length?void h(t):void(v.children().length&&v.remove())}function l(t){for(var n=v.children(),o=n.length-1;o>=0;o--)u(e(n[o]),t)}function u(t,n,o){var s=!(!o||!o.force)&&o.force;return!(!t||!s&&0!==e(":focus",t).length)&&(t[n.hideMethod]({duration:n.hideDuration,easing:n.hideEasing,complete:function(){h(t)}}),!0)}function d(t){return v=e("<div/>").attr("id",t.containerId).addClass(t.positionClass),v.appendTo(e(t.target)),v}function p(){return{tapToDismiss:!0,toastClass:"toast",containerId:"toast-container",debug:!1,showMethod:"fadeIn",showDuration:300,showEasing:"swing",onShown:void 0,hideMethod:"fadeOut",hideDuration:1e3,hideEasing:"swing",onHidden:void 0,closeMethod:!1,closeDuration:!1,closeEasing:!1,closeOnHover:!0,extendedTimeOut:1e3,iconClasses:{error:"toast-error",info:"toast-info",success:"toast-success",warning:"toast-warning"},iconClass:"toast-info",positionClass:"toast-top-right",timeOut:5e3,titleClass:"toast-title",messageClass:"toast-message",escapeHtml:!1,target:"body",closeHtml:'<button type="button">&times;</button>',closeClass:"toast-close-button",newestOnTop:!0,preventDuplicates:!1,progressBar:!1,progressClass:"toast-progress",rtl:!1}}function f(e){C&&C(e)}function g(t){function o(e){return null==e&&(e=""),e.replace(/&/g,"&amp;").replace(/"/g,"&quot;").replace(/'/g,"&#39;").replace(/</g,"&lt;").replace(/>/g,"&gt;")}function s(){c(),u(),d(),p(),g(),C(),l(),i()}function i(){var e="";switch(t.iconClass){case"toast-success":case"toast-info":e="polite";break;default:e="assertive"}I.attr("aria-live",e)}function a(){E.closeOnHover&&I.hover(H,D),!E.onclick&&E.tapToDismiss&&I.click(b),E.closeButton&&j&&j.click(function(e){e.stopPropagation?e.stopPropagation():void 0!==e.cancelBubble&&e.cancelBubble!==!0&&(e.cancelBubble=!0),E.onCloseClick&&E.onCloseClick(e),b(!0)}),E.onclick&&I.click(function(e){E.onclick(e),b()})}function r(){I.hide(),I[E.showMethod]({duration:E.showDuration,easing:E.showEasing,complete:E.onShown}),E.timeOut>0&&(k=setTimeout(b,E.timeOut),F.maxHideTime=parseFloat(E.timeOut),F.hideEta=(new Date).getTime()+F.maxHideTime,E.progressBar&&(F.intervalId=setInterval(x,10)))}function c(){t.iconClass&&I.addClass(E.toastClass).addClass(y)}function l(){E.newestOnTop?v.prepend(I):v.append(I)}function u(){if(t.title){var e=t.title;E.escapeHtml&&(e=o(t.title)),M.append(e).addClass(E.titleClass),I.append(M)}}function d(){if(t.message){var e=t.message;E.escapeHtml&&(e=o(t.message)),B.append(e).addClass(E.messageClass),I.append(B)}}function p(){E.closeButton&&(j.addClass(E.closeClass).attr("role","button"),I.prepend(j))}function g(){E.progressBar&&(q.addClass(E.progressClass),I.prepend(q))}function C(){E.rtl&&I.addClass("rtl")}function O(e,t){if(e.preventDuplicates){if(t.message===w)return!0;w=t.message}return!1}function b(t){var n=t&&E.closeMethod!==!1?E.closeMethod:E.hideMethod,o=t&&E.closeDuration!==!1?E.closeDuration:E.hideDuration,s=t&&E.closeEasing!==!1?E.closeEasing:E.hideEasing;if(!e(":focus",I).length||t)return clearTimeout(F.intervalId),I[n]({duration:o,easing:s,complete:function(){h(I),clearTimeout(k),E.onHidden&&"hidden"!==P.state&&E.onHidden(),P.state="hidden",P.endTime=new Date,f(P)}})}function D(){(E.timeOut>0||E.extendedTimeOut>0)&&(k=setTimeout(b,E.extendedTimeOut),F.maxHideTime=parseFloat(E.extendedTimeOut),F.hideEta=(new Date).getTime()+F.maxHideTime)}function H(){clearTimeout(k),F.hideEta=0,I.stop(!0,!0)[E.showMethod]({duration:E.showDuration,easing:E.showEasing})}function x(){var e=(F.hideEta-(new Date).getTime())/F.maxHideTime*100;q.width(e+"%")}var E=m(),y=t.iconClass||E.iconClass;if("undefined"!=typeof t.optionsOverride&&(E=e.extend(E,t.optionsOverride),y=t.optionsOverride.iconClass||y),!O(E,t)){T++,v=n(E,!0);var k=null,I=e("<div/>"),M=e("<div/>"),B=e("<div/>"),q=e("<div/>"),j=e(E.closeHtml),F={intervalId:null,hideEta:null,maxHideTime:null},P={toastId:T,state:"visible",startTime:new Date,options:E,map:t};return s(),r(),a(),f(P),E.debug&&console
// console.log(P)
    ,I}}function m(){return e.extend({},p(),b.options)}function h(e){v||(v=n()),e.is(":visible")||(e.remove(),e=null,0===v.children().length&&(v.remove(),w=void 0))}var v,C,w,T=0,O={error:"error",info:"info",success:"success",warning:"warning"},b={clear:r,remove:c,error:t,getContainer:n,info:o,options:{},subscribe:s,success:i,version:"2.1.3",warning:a};return b}()})}("function"==typeof define&&define.amd?define:function(e,t){"undefined"!=typeof module&&module.exports?module.exports=t(require("jquery")):window.toastr=t(window.jQuery)});
//# sourceMappingURL=toastr.js.map


/* eslint-disable no-magic-numbers, no-unused-vars */
var i = -1;
var toastCount = 0;
var $toastlast;

var getMessage = function getMessage() {
  var msgs = ['My name is Inigo Montoya. You killed my father. Prepare to die!', '<div><input class="input-small" value="textbox"/>&nbsp;<a href="http://johnpapa.net" target="_blank">This is a hyperlink</a></div><div><button type="button" id="okBtn" class="btn btn-primary">Close me</button><button type="button" id="surpriseBtn" class="btn" style="margin: 0 8px 0 8px">Surprise me</button></div>', 'Are you the six fingered man?', 'Inconceivable!', 'I do not think that means what you think it means.', 'Have fun storming the castle!'];
  i++;

  if (i === msgs.length) {
    i = 0;
  }
};

var getMessageWithClearButton = function getMessageWithClearButton(msg) {
  msg = msg ? msg : 'Clear itself?';
  msg += '<br /><br /><button type="button" class="btn clear">Yes</button>';
  return msg;
}; // eslint-disable-next-line complexity


$('#showtoast').click(function () {
  var shortCutFunction = $('#toastTypeGroup input:radio:checked').val();
  var msg = $('#message').val();
  var title = $('#title').val() || '';
  var $showDuration = $('#showDuration');
  var $hideDuration = $('#hideDuration');
  var $timeOut = $('#timeOut');
  var $extendedTimeOut = $('#extendedTimeOut');
  var $showEasing = $('#showEasing');
  var $hideEasing = $('#hideEasing');
  var $showMethod = $('#showMethod');
  var $hideMethod = $('#hideMethod');
  var toastIndex = toastCount++;
  var addClear = $('#addClear').prop('checked');
  toastr.options = {
    closeButton: $('#closeButton').prop('checked'),
    debug: $('#debugInfo').prop('checked'),
    newestOnTop: $('#newestOnTop').prop('checked'),
    progressBar: $('#progressBar').prop('checked'),
    positionClass: $('#positionGroup input:radio:checked').val() || 'toast-top-right',
    preventDuplicates: $('#preventDuplicates').prop('checked'),
    onclick: null
  };

  if ($('#addBehaviorOnToastClick').prop('checked')) {
    toastr.options.onclick = function () {
      // eslint-disable-next-line no-alert
      alert('You can perform some custom action after a toast goes away');
    };
  }

  if ($showDuration.val().length) {
    toastr.options.showDuration = $showDuration.val();
  }

  if ($hideDuration.val().length) {
    toastr.options.hideDuration = $hideDuration.val();
  }

  if ($timeOut.val().length) {
    toastr.options.timeOut = addClear ? 0 : $timeOut.val();
  }

  if ($extendedTimeOut.val().length) {
    toastr.options.extendedTimeOut = addClear ? 0 : $extendedTimeOut.val();
  }

  if ($showEasing.val().length) {
    toastr.options.showEasing = $showEasing.val();
  }

  if ($hideEasing.val().length) {
    toastr.options.hideEasing = $hideEasing.val();
  }

  if ($showMethod.val().length) {
    toastr.options.showMethod = $showMethod.val();
  }

  if ($hideMethod.val().length) {
    toastr.options.hideMethod = $hideMethod.val();
  }

  if (addClear) {
    msg = getMessageWithClearButton(msg);
    toastr.options.tapToDismiss = false;
  }

  if (!msg) {
    msg = getMessage();
  }
  /* eslint-disable prefer-template, operator-linebreak */


  $('#toastrOptions').text('Command: toastr["' + shortCutFunction + '"]("' + msg + (title ? '", "' + title : '') + '")\n\ntoastr.options = ' + JSON.stringify(toastr.options, null, 2));
  /* eslint-enable prefer-template, operator-linebreak */

  var $toast = toastr[shortCutFunction](msg, title); // Wire up an event handler to a button in the toast, if it exists

  $toastlast = $toast;

  if (typeof $toast === 'undefined') {
    return;
  }

  if ($toast.find('#okBtn').length) {
    $toast.delegate('#okBtn', 'click', function () {
      // eslint-disable-next-line no-alert
      alert("you clicked me. i was toast #" + toastIndex + ". goodbye!");
      $toast.remove();
    });
  }

  if ($toast.find('#surpriseBtn').length) {
    $toast.delegate('#surpriseBtn', 'click', function () {
      // eslint-disable-next-line no-alert
      alert("Surprise! you clicked me. i was toast #" + toastIndex + ". You could perform an action here.");
    });
  }

  if ($toast.find('.clear').length) {
    $toast.delegate('.clear', 'click', function () {
      toastr.clear($toast, {
        force: true
      });
    });
  }
});

var getLastToast = function getLastToast() {
  return $toastlast;
};

$('#clearlasttoast').click(function () {
  toastr.clear(getLastToast());
});
$('#cleartoasts').click(function () {
  toastr.clear();
});
toastr.options = {
  "closeButton": true,
  "debug": true,
  "newestOnTop": true,
  "progressBar": true,
  "positionClass": "toast-top-right",
  "preventDuplicates": true,
  "onclick": null,
  "showDuration": "300",
  "hideDuration": "1000",
  "timeOut": "5000",
  "extendedTimeOut": "1000",
  "showEasing": "swing",
  "hideEasing": "linear",
  "showMethod": "fadeIn",
  "hideMethod": "fadeOut"
};