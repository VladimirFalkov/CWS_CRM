/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    'client/templates/client/*.html',
    'core/templates/core/*.html',
    'core/templates/core/partials/*.html',
    'team/templates/team/*.html',
    'lead/templates/lead/*.html',
    'dashboard/templates/dashboard/*.html',
    'userprofile/templates/userprofile/*.html',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

