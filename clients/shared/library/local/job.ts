// Shared library
import api from '../server/api';
import { dp } from '../../components/routes/routes';

export const create_job_from_gui = async (
  title:string, client:string, location:string, min_salary:string, max_salary:string
) => {

  const job_title = encodeURIComponent(title);
  const job_client = encodeURIComponent(client);
  const job_location = encodeURIComponent(location);
  const job_min_salary = encodeURIComponent(min_salary);
  const job_max_salary = encodeURIComponent(max_salary);

  await api(
    `job/create/${job_title}/${job_client}/${job_location}/${job_min_salary}/${job_max_salary}`,
    (resp: any) => null,
    (resp: any) => window.location.href = dp(`jobs/${resp}`)
  );

}
