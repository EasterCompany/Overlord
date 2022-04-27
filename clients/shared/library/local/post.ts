// Shared library
import api from '../server/api';
import { dp } from '../../components/routes/routes';

export const create_post_from_gui = async (
  title:string, subheader:string, location:string, genre:string, link:string,
  custom_values:string, custom_tags:string
) => {

  const post_title = encodeURIComponent(title);
  const post_subheader = encodeURIComponent(subheader);
  const post_location = encodeURIComponent(location);
  const post_genre = encodeURIComponent(genre);
  const post_link = encodeURIComponent(link);
  const post_custom_values = encodeURIComponent(custom_values);
  const post_custom_tags = encodeURIComponent(custom_tags);

  await api(
    `post/create/${post_title}/${post_subheader}/${post_location}/${post_genre}/${post_link}` +
    `/${post_custom_values}/${post_custom_tags}`,
    (resp: any) => null,
    (resp: any) => window.location.href = dp(`posts/${resp}`)
  );

}


export default create_post_from_gui;
