import React from "react";
import gsap from "gsap";
const { useRef, useState, useEffect, createRef } = React;


/*--------------------
Items
--------------------*/
const items = [
{
  name: "Home",
  color: "#f44336",
  href: "#" },

{
  name: "Demo Application",
  color: "#e91e63",
  href: "#" },

{
  name: "Help",
  color: "#9c27b0",
  href: "#" },

{
  name: "Contact",
  color: "#673ab7",
  href: "#" },

{
  name: "Disclaimer",
  color: "#3f51b5",
  href: "#" }];




/*--------------------
Menu
--------------------*/
const Menu = ({ items }) => {
  const $root = useRef();
  const $indicator1 = useRef();
  const $indicator2 = useRef();
  const $items = useRef(items.map(createRef));
  const [active, setActive] = useState(0);

  useEffect(() => {

    const animate = () => {
      const menuOffset = $root.current.getBoundingClientRect();
      const activeItem = $items.current[active].current;
      const { width, height, top, left } = activeItem.getBoundingClientRect();
  
      const settings = {
        x: left - menuOffset.x,
        y: top - menuOffset.y,
        width: width,
        height: height,
        backgroundColor: items[active].color,
        ease: 'elastic.out(.7, .7)',
        duration: .8 };
  
  
      gsap.to($indicator1.current, {
        ...settings });
  
  
      gsap.to($indicator2.current, {
        ...settings,
        duration: 1 });
  
    };
    animate();
    window.addEventListener('resize', animate);

    return () => {
      window.removeEventListener('resize', animate);
    };
  }, [active, items]);

  return /*#__PURE__*/(
    React.createElement("div", {
      ref: $root,
      className: "menu" },

    items.map((item, index) => /*#__PURE__*/
    React.createElement("a", {
      key: item.name,
      ref: $items.current[index],
      className: `item ${active === index ? 'active' : ''}`,
      onMouseEnter: () => {
        setActive(index);
      },
      href: item.href },

    item.name)), /*#__PURE__*/


    React.createElement("div", {
      ref: $indicator1,
      className: "indicator" }), /*#__PURE__*/

    React.createElement("div", {
      ref: $indicator2,
      className: "indicator" })));



};

export default Menu;
export {items};
/*--------------------
App
--------------------*/
// const App = () => {
//   return /*#__PURE__*/(
//     React.createElement("div", { className: "App" }, /*#__PURE__*/
//     React.createElement(Menu, { items: items })));


// };
