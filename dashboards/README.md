# Grafana Dashboards for DevLake

This folder contains Grafana dashboards used to display data collected by [Apache DevLake](https://devlake.apache.org/). These dashboards provide essential insights into projects and help identify issues and opportunities for improvement.

## Repository Structure

The JSON files in this folder correspond to pre-configured Grafana dashboards. These dashboards can be directly imported into Grafana to display dynamic visualizations of DevLake data.

### Dashboard Descriptions

- **Error Dashboard**: Displays issues found in GitHub issue tracking, such as issues without type, description, or assignees. This panel helps ensure that issues are properly created, improving data quality.

- **SonarQube**: Shows data collected from [SonarQube](https://www.sonarqube.org/), a code quality analysis tool that detects vulnerabilities, bugs, and maintainability issues in project source code.

- **Throughput**: Displays the throughput of issues in GitHub projects from different analytical perspectives. Throughput is an essential metric as it measures the amount of work completed within a given period, helping to assess team productivity and identify bottlenecks in the development process.

## How to Import Dashboards

To import dashboards into Grafana, follow the steps below:

1. Open Grafana in your browser. The default link is `http://localhost:4000/grafana`.
2. Log in with your credentials.
3. In the side menu, click **Dashboards** > **New** > **Import**.
4. Select the desired `.json` dashboard file.
5. Fill in the required information, such as the data source.
6. Click **Import** to complete the import.

Your dashboard is now available for use in your Grafana environment.

## Customization

You can edit the dashboards directly in Grafana to better suit your project's needs. Modify panels, adjust data sources, and create new visualizations as needed.
