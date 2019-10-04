Rails.application.routes.draw do
  get 'welcome/page1'
  get 'welcome/page2'
  get 'welcome/index'

  root 'welcome#index'
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
end
