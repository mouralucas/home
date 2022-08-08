// package metadata file for Meteor.js

Package.describe({
  name: 'twbs:popper', // https://atmospherejs.com/twbs/bootstrap
  summary: 'The most popular front-end framework for developing responsive, mobile first projects on the web.',
  version: '4.4.1',
  git: 'https://github.com/twbs/bootstrap.git'
});

Package.onUse(function (api) {
  api.versionsFrom('METEOR@1.0');
  api.use('jquery', 'client');
  api.addFiles([
    'dist/css/popper.css',
    'dist/js/popper.js'
  ], 'client');
});
