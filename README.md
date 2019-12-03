Website
<%= image_tag('face.jpg', :style => 'border-right: 1px solid #000; display: block; margin-left: auto; margin-right:auto;width:50%', :size=>"20x300") %>
<p></p>
<p> </p>
<p> </p>
<p> </p>
<p> </p>
<b><p style ="font-size: 150%; ">Username: <%= current_user.email %></p></b>
<b><p style ="font-size: 150%;">Current Date: <%=Date.today.to_s%></p></b>
