/*
  Overlord Carousel Component

  To create a carousel, first import the <Carousel> and <CarouselItem> components from this file.
  then use the Carousel component like this:

  <Carousel>
    ...
  </Carousel>

  and wrap it around your Carousel Items, which behave similarly to a <img src="" alt=""/> component
*/

// React
import React, { useState } from "react";
// Assets
import "./carousel.css";


export const CarouselItem = (props:any) => {
  return <img
    className="ol-carousel-item"
    alt={props.alt}
    src={props.src}
    style={props.style}
  />
};


const Carousel = (props:any) => {
  const [ index, setIndex ] = useState(0);
  const [ isExpanded, setExpanded ] = useState(false);
  const offset = props.offset === undefined ? 100 : props.offset;

  const LeftBtn = props.leftButton;
  const RightBtn = props.rightButton;
  const ExpandBtn = props.expandButton;
  const ExitBtn = props.exitButton;

  const incrementIndex = (nextIndex:number) => {
    if (props.infiniteCycle !== undefined && props.infiniteCycle === true) {
      if (nextIndex < 0) nextIndex = React.Children.count(props.children) - 1;
      else if (nextIndex >= React.Children.count(props.children)) nextIndex = 0;
    } else {
      if (nextIndex < 0) nextIndex = 0;
      else if (nextIndex >= React.Children.count(props.children)) nextIndex = React.Children.count(props.children) - 1;
    }
    return setIndex(nextIndex);
  }

  return <div className="ol-carousel" style={
    isExpanded ?
      {
        position: 'fixed',
        top: '0',
        left: '0',
        width: '100vw',
        maxHeight: '100vh',
        zIndex: '99',
        overflowY: 'scroll',
        overflowX: 'hidden',
        margin: 'unset',
        padding: 'unset',
      }
    :
      {}
  }>

    <div className="ol-carousel-btns">
    {
      isExpanded ?
      <button onClick={() => setExpanded(false)} style={{
        position: 'fixed',
        top: '0',
        right: '0',
        pointerEvents: 'all'
      }}><ExitBtn/></button>
      : <></>
    }
      <button onClick={() => incrementIndex(index - 1)} style={
        isExpanded ?
          {
            position: 'fixed',
            top: 'calc(50% - 21px)',
            left: '0',
            pointerEvents: 'all'
          }
        :
          {
            pointerEvents: 'all'
          }
      }><LeftBtn/></button>
      <button onClick={() => incrementIndex(index + 1)} style={
        isExpanded ?
          {
            position: 'fixed',
            top: 'calc(50% - 21px)',
            right: '0',
            pointerEvents: 'all'
          }
        :
          {
            pointerEvents: 'all'
          }
      }><RightBtn/></button>
    </div>

    <div
      className="ol-carousel-image"
      style={{
        minHeight: isExpanded ? "100vh" : undefined,
        transform: `translateX(-${index * offset}%)`
      }}
    >
      {React.Children.map(props.children, (child:any) => {
        return React.cloneElement(child, {width: "100%"});
      })}
    </div>

    <div className="ol-carousel-indicators" style={
      isExpanded ?
        {
          display: 'none'
        }
      :
        {}
    }>
      {React.Children.map(props.children, (child:any, _index:number) => {
        return <span
          className={
            index === _index ? "ol-carousel-indicator ol-carousel-indicator-selected" : "ol-carousel-indicator"
          }
          style={{minWidth: `${100 / React.Children.count(props.children)}%`}}
        >&nbsp;</span>
      })}
    </div>

    {
      props.expandButton !== undefined && isExpanded !== true ?
        <button
          className="ol-carousel-expand-btn"
          onClick={() => setExpanded(true)}
        ><ExpandBtn/></button>
      :
        <></>
    }

  </div>
};


export default Carousel;
